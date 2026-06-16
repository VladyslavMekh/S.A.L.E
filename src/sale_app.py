import json
from typing import List

from stages.first.data_loader import DataLoader
from stages.second.student import Student
from stages.second.pipeline import Pipeline
from stages.third.analyzer import Analyzer


class SALEApp:
    def __init__(self, data_file: str, config_file: str):
        self.data_file = data_file
        self.config_file = config_file
        self.students: List[Student] = []

    def run(self):
        loader = DataLoader()
        raw_data = list(loader.load_data(self.data_file))

        self.students = [Student(d) for d in raw_data if d]

        pipeline = Pipeline(self.config_file)
        cleaned = pipeline.process(self.students)

        with open("/Users/vladyslavmekh/Desktop/S.A.L.E/src/data/output/s33307_quarantine.json", "w", encoding="utf-8") as f:
            json.dump(dict(pipeline.quarantine), f, indent=2, ensure_ascii=False)

        cleaned.sort(key=lambda s: (-s.avg_grade(), s.name))

        path_to_raport = "/Users/vladyslavmekh/Desktop/S.A.L.E/src/data/output/s33307_raport.json"
        Analyzer(cleaned, path_to_raport)

        print(f"Processing complete. Exported to s33307_raport.json")
        # print(f"Quarantine saved. Total processed: {len(cleaned)}")

        analyzer = Analyzer(cleaned, path_to_raport)
        analyzer.console_table()
        analyzer.visualizations()
