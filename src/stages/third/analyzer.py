from stages.second.student import Student
from matplotlib import pyplot as plt
from typing import List
import statistics
import pandas as pd


class Analyzer:
    def __init__(self, students: List[Student], output_json: str):
        data = []
        for student in students:
            d = student.to_dict()
            if 'grades_avg' not in d:
                d['grades_avg'] = student.avg_grade() if hasattr(student, 'avg_grade') else 0.0
            if 'grades_min' not in d:
                d['grades_min'] = min(student.grades) if student.grades else 0.0
            if 'grades_max' not in d:
                d['grades_max'] = max(student.grades) if student.grades else 0.0
            data.append(d)

        self.df = pd.DataFrame(data)
        self.output_json = output_json

        if not self.df.empty:
            self.df.to_json(output_json, orient='records', indent=2)

    def console_table(self):
        if self.df.empty:
            print("No data")
            return

        self.df['domain'] = self.df['email'].str.split('@').str[-1].str.lower()

        self.df['bucket'] = pd.cut(self.df['grades_avg'],
                                   bins=[0, 3.0, 4.0, 6.0],
                                   labels=['Zagrożeni', 'Przeciętni', 'Prymusi'],
                                   include_lowest=True)

        for bucket in ['Zagrożeni', 'Przeciętni', 'Prymusi']:
            subset = self.df[self.df['bucket'] == bucket]
            if subset.empty:
                continue
            grouped = subset.groupby('domain').agg({
                'grades_avg': 'mean',
                'grades_max': 'max',
                'id': 'count'
            }).round(2)
            print(f"\n=== {bucket} ===")
            print(grouped.to_string())

    def visualizations(self):
        if self.df.empty:
            print("No data for visualization")
            return

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        # Bar plot - TOP 10
        top10 = self.df.nlargest(10, 'grades_avg')
        colors = ['green' if row['grades_min'] >= 3.5 else 'red' for _, row in top10.iterrows()]
        axs[0].bar(range(len(top10)), top10['grades_avg'], color=colors)
        axs[0].set_title('TOP 10 Students by Average Grade')
        axs[0].set_xticks(range(len(top10)))
        axs[0].set_xticklabels(top10['name'], rotation=45, ha='right')

        # Pie chart
        domain_counts = self.df['domain'].value_counts()
        explode = [0.1 if i == 0 else 0 for i in range(len(domain_counts))]
        axs[1].pie(domain_counts, labels=domain_counts.index, autopct='%1.1f%%', explode=explode)
        axs[1].set_title('Email Domain Distribution')

        # Scatter
        self.df['variance'] = self.df['grades'].apply(
            lambda x: statistics.variance(x) if isinstance(x, list) and len(x) > 1 else 0
        )
        sizes = self.df['grades'].apply(lambda x: sum(x) * 5 if isinstance(x, list) else 0)

        axs[2].scatter(self.df['grades_avg'], self.df['variance'], s=sizes, alpha=0.7)
        axs[2].set_xlabel('Average Grade')
        axs[2].set_ylabel('Grade Variance')
        axs[2].set_title('Avg vs Variance')

        plt.tight_layout()
        plt.savefig('src/data/output/visualization.png')
        plt.show()