from dataclasses import dataclass

import bliss

@dataclass
class Student:
    firstname: str
    lastname: str

    school: bliss.School

    @property
    def name(self) -> str:
        return f"{firstname} {lastname}"
