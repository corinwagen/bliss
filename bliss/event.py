from __future__ import annotations

from dataclasses import dataclass, field

import bliss
import numpy as np
import pandas as pd

@dataclass
class SpeechEvent:
    name: str
    ballot_template: str
    posting_template: str
    students: list[bliss.Student] = field(default_factory=list)
    rounds: list[bliss.SpeechRound] = field(default_factory=list)

    def add_round(self, round_name, rooms, students=None, **kwargs):
        if students == None:
            students = self.students

        self.rounds.append(bliss.SpeechRound(self, round_name, rooms, students, **kwargs))
        return self.rounds[-1]

    def prelim_rankings(self, rounds=None):
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

@dataclass
class DebateEvent:
    name: str
    ballot_template: str
    posting_template: str
    teams: list[bliss.Team] = field(default_factory=list)
    rounds: list[bliss.SpeechRound] = field(default_factory=list)

    def add_round(self, round_name, rooms, teams=None, **kwargs):
        if teams == None:
            teams = self.teams

        self.rounds.append(bliss.DebateRound(self, round_name, rooms, teams, **kwargs))
        return self.rounds[-1]

    @property
    def students(self):
        studs = list()
        for team in self.teams:
            studs.append(team.students[0])
            studs.append(team.students[1])
        return studs

    def rankings(self, filename, speaker_filename, rounds):
        scores_by_team = np.zeros(shape=len(self.teams))
        num_scores = np.zeros(shape=len(self.teams))
        speaker_points = np.zeros(shape=len(self.students))

        # team results
        df = pd.read_excel(filename, header=[0,1], index_col=0)
        for idx, row in df.iterrows():
            for rd in rounds:
                if pd.isna(row[rd][1]):
                    continue

                if sum(row[rd]) > len(row[rd])/2:
                    scores_by_team[idx] += 1

                num_scores[idx] += 1

        # speaker pts
        df = pd.read_excel(speaker_filename, header=[0,1], index_col=0)
        for i, (idx, row) in enumerate(df.iterrows()):
            for rd in rounds:
                if pd.isna(row[rd][1]):
                    continue

                speaker_points[i] += sum(row[rd])

        # who's the best? # rounds, then # wins, then speaker pts
        speaker_points_by_team = np.array([self.avg_speaker_pts_by_team(idx, speaker_points) for idx in range(len(self.teams))])
        goodness = 100 * num_scores + scores_by_team + 0.001 * speaker_points_by_team
        team_order = np.argsort(goodness)[::-1]

        return team_order, scores_by_team, num_scores, speaker_points

    def print_rankings(self, *args):
        team_order, scores, num_scores, speaker_pts = self.rankings(*args)

        for idx in team_order:
            print(f"{self.teams[idx].name: <30} ({idx})\t{scores[idx]:}\t{int(num_scores[idx])}\t{self.avg_speaker_pts_by_team(idx, speaker_pts):.2f}")

        print("\n")

        student_order = np.argsort(speaker_pts)[::-1]
        for idx in student_order:
            print(f"{self.students[idx].name: <30}\t{speaker_pts[idx]}")

    def top_teams(self, num):
        team_order, num_scores, _ = self.rankings()

        top_teams = []
        for idx in team_order[:num]:
            top_teams.append(self.teams[idx])

        return top_teams

    def avg_speaker_pts_by_team(self, idx, speaker_pts):
        team = self.teams[idx]
        student_ids = []
        for student in team.students:
            student_ids.append(student.id)

        return np.mean(
            speaker_pts[
                [[s.id for s in self.students].index(i) for i in student_ids]
            ]
        )

