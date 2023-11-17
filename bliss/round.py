from dataclasses import dataclass, field
import bliss
import numpy as np
import copy
import random
import docx
import os
import yaml

@dataclass
class SpeechRound:
    name: str
    event: bliss.SpeechEvent
    rooms: list[str]
    students: list[bliss.Student]
    judges_per_room: int = 1
    write_prefix: str = "write/"

    assignments: list[list[bliss.Student]] = field(init=False)

    def __post_init__(self, event, name, rooms, students, judges_per_room=1, write_prefix="write/"):
        self.name = name
        self.rooms = rooms
        self.students = students
        self.judges_per_room = judges_per_room
        self.assignments = [[] for _ in self.rooms]
        self.ballots = [[] for _ in self.rooms]

        self.write_prefix = write_prefix

        self.event = event

    def __repr__(self):
        repr_str = f"SpeechRound {self.name}({self.num_rooms()} rooms, {len(self.students)} students, "

        if self.broken():
            repr_str += f"breaks complete, {self.ballots_complete()}/{self.num_ballots()} ballots)"
        else:
            repr_str += f"breaks incomplete, {self.ballots_complete()}/{self.num_ballots()} ballots)"

        return repr_str

    def do_break(self, randomize=True):
        if self.broken():
            print("Already broken!")
            return

        shuffled_students = copy.deepcopy(self.students)
        if randomize:
            random.shuffle(shuffled_students)
        else:
            print("not randomizing!")

        # assign students
        for idx, student in enumerate(shuffled_students):
            assignment_idx = idx % len(self.assignments)
            self.assignments[assignment_idx].append(student)

        print("Round broken!")

    def num_rooms(self):
        return len(self.rooms)

    def gen_ballots(self):
        for idx, room in enumerate(self.rooms):
            for judge_id in range(1, self.judges_per_room + 1):
                save_str = f"{self.write_prefix}{self.event.name}_Round{self.name}_Room{idx}_Ballot{judge_id}.docx"
                if os.path.exists(save_str):
                    print(f"Already file at {save_str} !")
                    return

                # from Walker
                temp = docx.Document(self.event.ballot_template)
                temp.paragraphs[2].text += self.name
                temp.paragraphs[4].text += f"{room} ({idx})"
                temp.paragraphs[6].text += f" ({judge_id})"
                table = temp.tables[0]

                for student_idx, student in enumerate(self.assignments[idx]):
                    table.cell(student_idx + 1, 0).text = f"{student} ({self.event.get_student_id(student)})"

                temp.save(save_str)

    def gen_postings(self):
        save_str = f"{self.write_prefix}{self.event.name}_Round{self.name}_Postings.docx"
        if os.path.exists(save_str):
            print(f"Already file at {save_str} !")
            return

        # from Walker
        temp = docx.Document(self.event.posting_template)
        temp.paragraphs[3].text += self.name
        table = temp.tables[0]

        for idx, room in enumerate(self.rooms):
            table.cell(0, idx).text += f" {room} ({idx})"
            for student_idx, student in enumerate(self.assignments[idx]):
                table.cell(student_idx + 1, idx).text = f"{student} ({self.event.get_student_id(student)})"

        temp.save(save_str)

    def num_ballots(self):
        return self.judges_per_room * self.num_rooms()

    def ballots_complete(self):
        return sum([len(b) for b in self.ballots])

    def broken(self):
        return any([len(a) for a in self.assignments])

    def add_ballot(self, yaml_file):
        ballot_info = dict()
        with open(yaml_file, "r+") as f:
            ballot_info = yaml.safe_load(f)

        # some validation
        for ballot in self.ballots[ballot_info["room_id"]]:
            if ballot.judge_id == ballot_info["judge_id"]:
                raise ValueError(f"judge {ballot_info['judge_id']} already has ballot entered for this room!")

        ballot = bliss.SpeechBallot(**ballot_info)
        self.ballots[ballot_info["room_id"]].append(ballot)

    def get_ranking_for_room(self, room_id):
        # returns dict mapping from student ids to placing

        ballots = self.ballots[room_id]

        # presumes all ballots have same order
        scores = np.zeros_like(ballots[0].student_ids, dtype=np.float64)
        for ballot in ballots:
            scores += 1/ballot.rankings

        # awkward
        scores_dict = {ballots[0].student_ids[i]: scores[i] for i in range(len(scores))}
        sorted_scores = {k: v for k, v in sorted(scores_dict.items(), key=lambda item: item[1], reverse=True)}

        # this is straight from stackoverflow
        positions = {}
        cur_score = None # Score we're examining
        cur_count = 0 # Number of others that we've seen with this score

        for ix, (name, score) in enumerate(sorted_scores.items()):
            if score == cur_score: # Same score for this player as previous
                cur_count += 1
            else: # Different score from before
                cur_score = score
                cur_count = 0
            positions[name] = ix - cur_count + 1 # Add 1 because ix is 0-based

        return positions


class DebateRound:
    def __init__(self, event, name, rooms, teams, judges_per_room=1, write_prefix="write/"):
        self.name = name
        self.rooms = rooms
        self.teams = teams
        self.judges_per_room = judges_per_room
        self.assignments = [[] for _ in self.rooms]
        self.ballots = [[] for _ in self.rooms]

        self.write_prefix = write_prefix

        self.event = event

    def __repr__(self):
        repr_str = f"DebateRound {self.name}({self.num_rooms()} rooms, {len(self.teams)} teams, "

        if self.broken():
            repr_str += f"breaks complete, {self.ballots_complete()}/{self.num_ballots()} ballots)"
        else:
            repr_str += f"breaks incomplete, {self.ballots_complete()}/{self.num_ballots()} ballots)"

        return repr_str

    def add_ballot(self, yaml_file):
        ballot_info = dict()
        with open(yaml_file, "r+") as f:
            ballot_info = yaml.safe_load(f)

        # some validation
        for ballot in self.ballots[ballot_info["room_id"]]:
            if ballot.judge_id == ballot_info["judge_id"]:
                raise ValueError(f"judge {ballot_info['judge_id']} already has ballot entered for this room!")

        ballot = bliss.DebateBallot(**ballot_info)
        self.ballots[ballot_info["room_id"]].append(ballot)

    def num_ballots(self):
        return self.judges_per_room * self.num_rooms()

    def ballots_complete(self):
        return sum([len(b) for b in self.ballots])

    def broken(self):
        return any([len(a) for a in self.assignments])

    def do_break(self, pairings=None):
        if self.broken():
            print("Already broken!")
            return

        if pairings is None:
            shuffled_students = copy.deepcopy(self.teams)
            random.shuffle(shuffled_students)

            # assign students
            for idx, student in enumerate(shuffled_students):
                assignment_idx = idx % len(self.assignments)
                self.assignments[assignment_idx].append(student)

        else:
            assert len(pairings) == len(self.rooms)
            for idx, room in enumerate(self.rooms):
                self.assignments[idx].append(self.teams[pairings[idx][0]])
                self.assignments[idx].append(self.teams[pairings[idx][1]])

        print("Round broken!")

    def gen_ballots(self):
        for idx, room in enumerate(self.rooms):
            for judge_id in range(1, self.judges_per_room + 1):
                save_str = f"{self.write_prefix}{self.event.name}_Round{self.name}_Room{idx}_Ballot{judge_id}.docx"
                if os.path.exists(save_str):
                    print(f"Already file at {save_str} !")
                    return

                temp = docx.Document(self.event.ballot_template)
                temp.paragraphs[2].text += self.name
                temp.paragraphs[4].text += f"{room} ({idx})"
                temp.paragraphs[6].text += f" ({judge_id})"

                team_table = temp.tables[0]
                student_table = temp.tables[1]
                student_counter = 1
                for team_idx, team in enumerate(self.assignments[idx]):
                    team_table.cell(team_idx + 1, 0).text = f"{team.name} ({self.event.get_team_id(team)})"
                    for student in team.students:
                        student_table.cell(student_counter, 0).text = f"{student} ({self.event.get_student_id(student)})"
                        student_counter += 1

                temp.save(save_str)

    def gen_postings(self):
        save_str = f"{self.write_prefix}{self.event.name}_Round{self.name}_Postings.docx"
        if os.path.exists(save_str):
            print(f"Already file at {save_str} !")
            return

        temp = docx.Document(self.event.posting_template)
        temp.paragraphs[3].text += self.name
        table = temp.tables[0]

        for idx, room in enumerate(self.rooms):
            table.cell(idx+1, 0).text += f" {room} ({idx})"
            aff_team = self.assignments[idx][0]
            neg_team = self.assignments[idx][1]
            table.cell(idx+1, 1).text = f"{aff_team.name} ({self.event.get_team_id(aff_team)})"
            table.cell(idx+1, 2).text = f"{neg_team.name} ({self.event.get_team_id(neg_team)})"

        temp.save(save_str)

    def num_rooms(self):
        return len(self.rooms)
