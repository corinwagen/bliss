import bliss
import numpy as np

class SpeechEvent:
    def __init__(self, name, students_list):
        self.rounds = []
        self.students = []
        pass

    def add_round(self, round_name, rooms, students=None):
        if students = None:
            students = self.students

        self.rounds.append(bliss.Round(name, rooms, students))

    def rankings(self, rounds=None):
        pass

    def gen_ballots_and_postings(self, round_name=None):
        pass
