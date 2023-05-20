class Team:
    def __init__(self, name, students):
        self.name = name
        self.students = students

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
