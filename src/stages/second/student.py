from typing import Dict, Any, List

class Student:      # In this class performs data mapping.

    def __init__(self, data: Dict[str, Any]):
        self.raw = data
        self.name: str = data.get("name", "NO DATA")
        self.id: str = data.get("id", "")
        self.address: str = data.get("address", "")
        self.grades: List[float] = data.get("grades", [])
        self.phone: str = data.get("phone", "")
        self.email: str = data.get("email", "")


    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "id": self.id,
            "address": self.address,
            "grades": self.grades,
            "phone": self.phone,
            "email": self.email,
        }


    def avg_grade(self) -> float:
        if not self.grades:
            return 0.0
        valid = [g for g in self.grades if isinstance(g, (int, float))]
        return round(sum(valid) / len(valid), 2) if valid else 0.0


    def __str__(self) -> str:
        return f"{self.name} ({self.id}) - Avg: {self.avg_grade():.1f}"