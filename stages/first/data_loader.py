from stages.first.decorators.count_lines_decorator import count_lines_decorator
from typing import Generator, Any
from stages.first.log_parser import *

class DataLoader:

    # Takes the path to the file with unsorted logs. In our case it is s33307.usrlog.

    @staticmethod       # Used to access this method without creating an object.
    @count_lines_decorator
    def load_data(file_path: str) -> Generator[dict[str, Any] | None, None, None]:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()     # Removing invisible characters (spaces, tabs, line breaks).
                if line:
                    parsed = LogParser.parse_line(line)
                    if parsed.get("name") and  parsed.get("id") and parsed.get("address") and parsed.get("grades") and (parsed.get("phone") or parsed.get("email")):
                        yield parsed
                    else:
                        yield None