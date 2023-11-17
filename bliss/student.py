from __future__ import annotations

from dataclasses import dataclass

import bliss

@dataclass
class Student:
    firstname: str
    lastname: str
    id: int

    school: bliss.School

    @property
    def name(self) -> str:
            return f"{self.firstname} {self.lastname}"
