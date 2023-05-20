import numpy as np
import copy
import random
import docx

class Round:
    def __init__(self, name, rooms, students, judges_per_room=1):
        self.name = name
        self.rooms = rooms
        self.students = students
        self.judges_per_room = judges_per_room
        self.assignments = [[] for _ in self.rooms]
        self.ballots = [[] for _ in self.rooms]

    def __repr__(self):
        repr_str = f"Round {self.name}({self.num_rooms()} rooms, {len(self.students)} students, "

        if self.broken():
            repr_str += f"breaks complete, {self.ballots_outstanding()}/{self.num_ballots()} ballots)"
        else:
            repr_str += f"breaks incomplete, {self.ballots_outstanding()}/{self.num_ballots()} ballots)"

        return repr_str

    def break(self, judges_per_room=1):
        shuffled_students = random.shuffle(copy.deepcopy(students))

        for idx, student in enumerate(shuffled_student):
            assignment_idx = idx % len(self.assignments)
            self.assignments[assignment_idx].append(student)

        print("Round broken!")

    def num_rooms(self):
        return len(self.rooms)

    def gen_ballots(self):
        print("NOT IMPLEMENTED YET!")

    def gen_postings(self):
        print("NOT IMPLEMENTED YET!")

    def num_ballots(self):
        return self.judges_per_room * self.num_rooms()

    def ballots_outstanding(self):
        return self.num_ballots() - sum([len(b) for b in self.ballots])
