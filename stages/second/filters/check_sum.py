import re
from stages.second.student import Student

class CheckSum:

    @staticmethod
    def run(student: Student) -> bool:
        if not student.id or not student.id.startswith("STU-"):
            return False

        match = re.search(r"STU-(\d{6})", student.id)
        if not match:
            return False

        digits_str = match.group(1)
        digits = [int(d) for d in digits_str]
        if len(digits) != 6:
            return False

        weighted = sum(d * (i + 1) for i, d in enumerate(digits[:-1]))
        control = digits[-1]
        return (weighted % 10) == control

    @staticmethod
    def repair(student: Student) -> Student:
        if student.id and "STU-" in student.id:
            match = re.search(r"STU-(\d+)", student.id)
            if match:
                core = match.group(1)
                reversed_core = core[::-1]
                student.id = f"STU-{reversed_core}"
        return student