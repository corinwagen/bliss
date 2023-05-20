import bliss
import numpy as np

class SpeechEvent:
    def __init__(self, name, students_list, ballot_template, posting_template):
        self.name = name
        self.ballot_template = ballot_template
        self.posting_template = posting_template
        self.rounds = []
        self.students = students_list
        pass

    def add_round(self, round_name, rooms, students=None, **kwargs):
        if students == None:
            students = self.students

        self.rounds.append(bliss.SpeechRound(self, round_name, rooms, students, **kwargs))

        return self.rounds[-1]

    def rankings(self, rounds=None):
        if isinstance(rounds, int):
            rounds = [self.rounds[rounds]]
        elif isinstance(rounds, str):
            rounds = [self.rounds[self.rounds.index(rounds)]]
        elif rounds is None:
            rounds = self.rounds

        scores_by_student = np.zeros(shape=len(self.students))
        num_scores_for_student = np.zeros(shape=len(self.students))

        for r in rounds:
            for ballot_room in r.ballots:
                for ballot in ballot_room:
                    for student_id, ranking in zip(ballot.student_ids, ballot.rankings):
                        scores_by_student[student_id] += 1/ranking
                        num_scores_for_student[student_id] += 1

        return scores_by_student, num_scores_for_student

    def print_rankings(self, rounds=None):
        scores, num_scores = self.rankings(rounds=rounds)
        student_order = np.argsort(scores)[::-1]
        for idx in student_order:
            print(f"{self.students[idx]: <16}\t{scores[idx]}\t{int(num_scores[idx])}")

    def top_students(self, num, rounds=None):
        scores, num_scores = self.rankings(rounds=rounds)
        student_order = np.argsort(scores)[::-1]

        top_students = []
        for idx in student_order[:num]:
            top_students.append(self.students[idx])

        return top_students

    def get_student_id(self, student):
        return self.students.index(student)

class DebateEvent:
    def __init__(self, name, teams, ballot_template, posting_template):
        self.name = name
        self.ballot_template = ballot_template
        self.posting_template = posting_template
        self.rounds = []
        self.teams = teams

        self.students = []
        for team in self.teams:
            self.students += team.students

    def add_round(self, round_name, rooms, teams=None, **kwargs):
        if teams == None:
            teams = self.teams

        self.rounds.append(bliss.DebateRound(self, round_name, rooms, teams, **kwargs))

        return self.rounds[-1]

    def rankings(self, rounds=None):
        if isinstance(rounds, int):
            rounds = [self.rounds[rounds]]
        elif isinstance(rounds, str):
            rounds = [self.rounds[self.rounds.index(rounds)]]
        elif rounds is None:
            rounds = self.rounds

        scores_by_team = np.zeros(shape=len(self.teams))
        num_scores = np.zeros(shape=len(self.teams))
        speaker_points = np.zeros(shape=self.num_speakers())

        for r in rounds:
            for ballot_room in r.ballots:
                for ballot in ballot_room:
                    for team_id, ranking in zip(ballot.team_ids, ballot.rankings):
                        # we only count wins here
                        if ranking == 1:
                            scores_by_team[team_id] += 1

                        num_scores[team_id] += 1

                    for student_id, speaker_pt in zip(ballot.student_ids, ballot.speaker_points):
                        speaker_points[student_id] += speaker_pt

        return scores_by_team, num_scores, speaker_points

    def print_rankings(self, rounds=None):
        scores, num_scores, speaker_pts = self.rankings(rounds=rounds)
        team_order = np.argsort(scores)[::-1]
        for idx in team_order:
            print(f"{self.teams[idx].name: <30} ({idx})\t{scores[idx]:}\t{int(num_scores[idx])}\t{self.avg_speaker_pts_by_team(idx):.2f}")

        print("\n")

        student_order = np.argsort(speaker_pts)[::-1]
        for idx in student_order:
            print(f"{self.students[idx]: <30}\t{speaker_pts[idx]}")

    def top_teams(self, num, rounds=None):
        scores, num_scores, _ = self.rankings(rounds=rounds)
        team_order = np.argsort(scores)[::-1]

        top_teams = []
        for idx in team_order[:num]:
            top_teams.append(self.teams[idx])

        return top_teams

    def get_student_id(self, student):
        return self.students.index(student)

    def get_team_id(self, team):
        return self.teams.index(team)

    def num_speakers(self):
        return sum([len(t.students) for t in self.teams])

    def avg_speaker_pts_by_team(self, idx, rounds=None):
        team = self.teams[idx]
        student_ids = []
        for student in team.students:
            student_ids.append(self.get_student_id(student))

        _, _, speaker_pts = self.rankings(rounds=rounds)
        return np.mean(speaker_pts[student_ids])

