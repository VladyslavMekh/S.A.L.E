from stages.second.student import Student
from typing import Tuple
import pandas as pd
import statistics

class GradeMapper():

    @staticmethod
    def run(student: Student) -> Tuple[bool, Student]:
        valid_grades = []
        for grade in student.grades:
            try:
                value = float(str(grade).replace(",", "."))
                if 1.0 <= value <= 6.0:
                    valid_grades.append(round(value, 1))
                else:
                    valid_grades.append(float("nan"))
            except (ValueError, TypeError):
                valid_grades.append(float("nan"))

        if not valid_grades:
            student.grades = [float("nan")]
            return False, student
        student.grades = valid_grades
        return True, student


    @staticmethod
    def repair(student: Student) -> Student:
        if not student.grades:
            return student

        valid = [grade for grade in student.grades if not pd.isna(grade)]
        nans = [grade for grade in student.grades if pd.isna(grade)]

        if len(nans) == 1 and valid:
            mean_value = round(statistics.mean(valid), 1)
            student.grades = [mean_value if pd.isna(grade) else grade for grade in student.grades]
        return student