from dataclasses import dataclass

import bliss

@dataclass
class Team:
    students: list[bliss.Student]

    @property
    def name (self) -> str:
        return "-".join([s.lastname for s in self.students])
