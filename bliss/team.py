from __future__ import annotations

from dataclasses import dataclass

import bliss

@dataclass
class Team:
    students: list[bliss.Student]
    id: int

    num_aff: int = 0

    @property
    def name (self) -> str:
        return "-".join([s.lastname for s in self.students])
