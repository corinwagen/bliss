from dataclasses import dataclass

import bliss

class Tournament:
    name: str
    schools: list[bliss.School]
    students: list[bliss.Student]
    events: list[bliss.Event]
