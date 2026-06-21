from stages.second.student import Student
import re

class CheckType():

    @staticmethod
    def run(student: Student) -> bool:
        if student.phone:
            clean_phone = re.sub(r"[^\d+]", "", student.phone)
            if not clean_phone:
                return False

        if student.email:
            if student.email.count('@') != 1 or '..' in student.email:
                return False

        if not all(isinstance(g, (int, float)) or str(g).replace(".", "").isdigit() for g in student.grades):
            return False
        return True


    @staticmethod
    def repair(student: Student) -> Student:
        if student.phone:
            student.phone = re.sub(r"[^\d+]", "", student.phone)
        if student.email:
            student.email = re.sub(r"[^a-zA-Z0-9@._-]", "", student.email)
            student.email = re.sub(r"@{2,}", r"@", student.email)
        return student