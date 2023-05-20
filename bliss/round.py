import bliss
import numpy as np
import copy
import random
import docx
import os
import yaml

class Round:
    def __init__(self, event, name, rooms, students, judges_per_room=1, write_prefix="write/"):
        self.name = name
        self.rooms = rooms
        self.students = students
        self.judges_per_room = judges_per_room
        self.assignments = [[] for _ in self.rooms]
        self.ballots = [[] for _ in self.rooms]

        self.write_prefix = write_prefix

        self.event = event

    def __repr__(self):
        repr_str = f"Round {self.name}({self.num_rooms()} rooms, {len(self.students)} students, "

        if self.broken():
            repr_str += f"breaks complete, {self.ballots_complete()}/{self.num_ballots()} ballots)"
        else:
            repr_str += f"breaks incomplete, {self.ballots_complete()}/{self.num_ballots()} ballots)"

        return repr_str

    def do_break(self, judges_per_room=1):
        if self.broken():
            print("Already broken!")
            return

        shuffled_students = copy.deepcopy(self.students)
        random.shuffle(shuffled_students)

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
                temp.paragraphs[5].text += f" ({judge_id})"
                table = temp.tables[0]

                for student_idx, student in enumerate(self.assignments[idx]):
                    table.cell(student_idx + 1, 0).text = f"{student} ({self.event.get_student_id(student)})"

                temp.save(save_str)

    def gen_postings(self):
        print("NOT IMPLEMENTED YET!")

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

        ballot = bliss.Ballot(**ballot_info)
        self.ballots[ballot_info["room_id"]].append(ballot)

