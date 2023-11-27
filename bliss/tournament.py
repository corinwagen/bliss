from __future__ import annotations

from dataclasses import dataclass
import bliss


@dataclass
class Tournament:
    name: str
    schools: list[bliss.School]
    students: list[bliss.Student]
    events: list[bliss.Event]
