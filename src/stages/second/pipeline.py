from stages.second.filters.check_type import CheckType
from stages.second.filters.check_required import CheckRequired
from stages.second.filters.check_sum import CheckSum
from stages.second.filters.deduplicate import Deduplicate
from stages.second.filters.grade_mapper import GradeMapper
from stages.second.filters.normalize import Normalize
from stages.second.student import Student
from collections import defaultdict
from typing import Dict, List
import json

class Pipeline:
    def __init__(self, config_path: str):
        self.steps = self.load_config(config_path)
        self.quarantine: Dict[str, List[Dict]] = defaultdict(list)
        self.seen_ids = set()

    @staticmethod
    def load_config(config_path: str) -> List[Dict]:
        with open(config_path, "r") as file:
            return json.load(file)

    def process(self, students: List[Student]) -> List[Student]:
        processed = []
        for student in students:
            current_student = student
            passed = True

            for step in self.steps:
                step_name = step["name"].upper()
                repair = step.get("repair", False)

                if step_name == "CHECK_TYPE":
                    if not CheckType.run(current_student):
                        if repair:
                            current_student = CheckType.repair(current_student)
                            if not CheckType.run(current_student):
                                self.quarantine["CHECK_TYPE"].append(current_student.to_dict())
                                passed = False
                                break
                        else:
                            self.quarantine["CHECK_TYPE"].append(current_student.to_dict())
                            passed = False
                            break

                elif step_name == "CHECK_REQUIRED":
                    args = ["id", "name", "address"]
                    if not CheckRequired.run(current_student, args):
                        self.quarantine['CHECK_REQUIRED'].append(current_student.to_dict())
                        passed = False
                        break

                elif step_name == 'NORMALIZE':
                    current_student = Normalize.run(current_student)

                elif step_name == 'GRADE_MAPPER':
                    success, current_student = GradeMapper.run(current_student)
                    if not success and repair:
                        current_student = GradeMapper.repair(current_student)
                        success, current_student = GradeMapper.run(current_student)

                    if not success:
                        self.quarantine['GRADE_MAPPER'].append(current_student.to_dict())
                        passed = False
                        break

                elif step_name == 'DEDUPLICATE':
                    if not Deduplicate.run(current_student, self.seen_ids):
                        self.quarantine['DEDUPLICATE'].append(current_student.to_dict())
                        passed = False
                        break

                elif step_name == 'CHECKSUM':
                    if not CheckSum.run(current_student):
                        if repair:
                            current_student = CheckSum.repair(current_student)
                            if not CheckSum.run(current_student):
                                self.quarantine['CHECKSUM'].append(current_student.to_dict())
                                passed = False
                                break
                        else:
                            self.quarantine['CHECKSUM'].append(current_student.to_dict())
                            passed = False
                            break
            if passed:
                processed.append(current_student)
        return processed