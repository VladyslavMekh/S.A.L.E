from stages.second.student import Student

class Deduplicate():

    @staticmethod
    def run(student: Student, seen: set) -> bool:
        key_first = student.id
        key_second = student.name.lower()
        if key_first in seen or key_second in seen:
            return False
        seen.add(key_first)
        seen.add(key_second)
        return True