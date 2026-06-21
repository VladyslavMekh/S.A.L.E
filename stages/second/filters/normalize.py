from stages.second.student import Student
import re

class Normalize:
    numbers_telugu = {
        "౦": "0", "౧": "1", "౨": "2", "౩": "3", "౪": "4", "౫": "5", "౬": "6", "౭": "7", "౮": "8", "౯": "9"
    }

    lower_case_numbers = {
        "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9"
    }

    @staticmethod
    def run(student: Student) -> Student:
        if student.name and student.name != "NO DATA":
            parts = re.split(r"[\s-]+", student.name)
            student.name = " ".join(p.capitalize() for p in parts if p)

        if student.address:
            parts = re.split(r"[\s-]+", student.address)
            student.address = " ".join(p.capitalize() for p in parts if p)

        if student.email:
            student.email = student.email.lower().strip()

        if student.phone:
            trans = str.maketrans(Normalize.numbers_telugu)
            student.phone = student.phone.translate(trans)
            if re.match("^\\+?48", student.phone):
                student.phone = re.sub(r"\+?48\s*(\d+)", r"(+48) \1", student.phone)

        if student.grades:
            trans = str.maketrans(Normalize.lower_case_numbers)
            cleaned_grades = []
            for grade in student.grades:
                grade_str = str(grade).translate(trans)
                try:
                    if grade_str:
                        cleaned_grades.append(round(float(grade_str), 1))
                except ValueError:
                    continue

            student.grades = cleaned_grades
        return student