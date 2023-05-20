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

    def add_round(self, round_name, rooms, students=None):
        if students == None:
            students = self.students

        self.rounds.append(bliss.Round(self, round_name, rooms, students))

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
