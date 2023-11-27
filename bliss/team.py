from __future__ import annotations

from dataclasses import dataclass, field

import bliss


@dataclass
class Team:
    students: list[bliss.Student]
    id: int

    # state
    num_aff: int = 0
    prev_seen: list[bliss.Team] = field(default_factory=list)

    @property
    def name(self) -> str:
        return "-".join([s.lastname for s in self.students])
