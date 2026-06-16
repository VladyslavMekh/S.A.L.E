from typing import Dict, Any
import re

class LogParser:

    @staticmethod
    def parse_line(line: str) -> Dict[str, Any]:
        data = {"name": "", "id": "", "address": "", "grades": [], "phone": "", "email": ""}

        address_match = re.search(r"(?i)addr(?:->|-|=)\s*([A-ZĄŁĘÓŚĆŻŹŃa-złąęóśćźń]+(?:-[A-ZĄŁĘÓŚĆŻŹŃa-ązłęóśćźń]+)?)", line, re.I)
        if address_match:
            data["address"] = address_match.group(1)

        id_match = re.search(r"(?i)ident(?:->|-|=)\s*(STU-(\d.{5}))", line, re.I)
        if id_match:
            data["id"] = id_match.group(1)

        name_match = re.search(r"(?i)user(?:->|-|=)\s*([A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż]+(?:[- ]+[A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż]+)*)", line, re.I)
        if name_match:
            data["name"] = name_match.group(1)

        grades_match = re.search(r"(?i)grades(?:->|-|=)\s*([^#|!|~| |\n]+)", line, re.I)
        if grades_match:
            grades_str = grades_match.group(1)

            subscript_map = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
            grades_str = grades_str.translate(subscript_map)
            grades_tokens = re.findall(r"\d+(?:\.\d+)?", grades_str)
            for grade in grades_tokens:
                try:
                    cleaned = re.sub(r"[^\d.]", "", grade).strip(".")
                    if cleaned:
                        value = float(cleaned)
                        if 1.0 <= value <= 5.0:
                            data["grades"].append(value)
                except ValueError:
                    pass



        phone_match = re.search(r"(?i)phone:(\+?[0-9౦౧౨౩౪౫౬౭౮౯\s-]+)", line, re.I)
        if phone_match:
            data["phone"] = phone_match.group(1).strip()

        email_match = re.search(r"(?i)email:([a-z0-9._%]+@[a-z0-9.-]+)", line, re.I)
        if email_match:
            data["email"] = email_match.group(1)

        return data