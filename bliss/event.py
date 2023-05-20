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

    def rankings(self, rounds=None):
        if isinstance(rounds, int):
            rounds = [self.rounds[rounds]]
        if rounds is None:
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

    def get_student_id(self, student):
        return self.students.index(student)
