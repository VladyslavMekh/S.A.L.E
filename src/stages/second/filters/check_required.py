from stages.second.student import Student
from typing import List

class CheckRequired:

    @staticmethod
    def run(student: Student, required: List[str]) -> bool:
        for field in required:
            value = getattr(student, field, None)
            if value is None:
                return False
            if str(value).strip().lower() in ["none", "n/a", "nan", "null", "", "no data"]:
                return False
        return True