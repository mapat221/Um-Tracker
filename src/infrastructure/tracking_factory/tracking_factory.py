from pathlib import Path
import csv
from .structures import student_result, subject_result
from . import errors
import random
from datetime import datetime


class TrackingFactory:
    _TEMPLATES_PATH = Path(__file__).parent / "templates" / "tracking.txt"

    def __init__(self):
        self._table: list[dict] = []

    def get_results(self, table_path: Path) -> str:
        try:
            with open(table_path, "r", encoding="utf-8") as table:
                reader = csv.DictReader(table)
                data = list(reader)
                self._table = data
        except Exception as e:
            raise errors.ReadTableError(f"Failed to read table, reason: {e}")

        all_students_results = self._compare_students()
        message = self._create_message(all_students_results)
        return message

    def _compare_students(self) -> list[student_result]:
        all_students: list[student_result] = []
        done_students = set()

        for row in self._table:
            student_name = row.get("ФИО ученика")

            if student_name and student_name not in done_students:
                student = student_result(
                    student_name=student_name,
                    subjects_results=self._get_student_subjects(student_name),
                )
                all_students.append(student)
                done_students.add(student_name)

        return all_students

    def _get_student_subjects(self, student_name: str) -> list[subject_result]:
        student_subjects = []
        for row in self._table:
            if row.get("ФИО ученика") == student_name:
                subject = subject_result(
                    name=row["Предметы"],
                    webinars=float(row["Ср.просмотренность"].replace(",", ".")),
                    homeworks=float(
                        row["Ср.сдаваемость - только регулярные дз"].replace(",", ".")
                    ),
                )
                student_subjects.append(subject)

        return student_subjects

    def _load_templates(self) -> dict[str, list[str]]:
        templates = {}
        current = None
        with open(self._TEMPLATES_PATH, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line.startswith("!"):
                    current = line[1:].lower()
                    templates[current] = []
                elif line and current:
                    templates[current].append(line)

        return templates

    def _create_message(self, all_students: list[student_result]) -> str:
        templates = self._load_templates()
        messages = []
        for student in all_students:
            name = student.student_name.split()[1]
            hello_message = random.choice(templates["приветствие"])
            again_message = random.choice(templates["снова"])

            today = datetime.now().day
            if today < 20:
                goal_key = "промежуточные"
                conclusion_key = "промежуточные планы"
            else:
                goal_key = "итоговые"
                conclusion_key = "итоговые планы"
            goal_message = random.choice(templates[goal_key])

            webinars_total = []
            homeworks_total = []
            for subject in student.subjects_results:
                webinars_total.append(subject.webinars)
                homeworks_total.append(subject.homeworks)
            if (
                sum(webinars_total) / len(webinars_total) >= 0.75
                or sum(homeworks_total) / len(homeworks_total) >= 0.75
            ):
                advice = random.choice(templates["отлично"])
            elif (
                sum(webinars_total) / len(webinars_total) >= 0.2
                or sum(homeworks_total) / len(homeworks_total) >= 0.2
            ):
                advice = random.choice(templates["хорошо"])
            else:
                advice = random.choice(templates["плохо"])

            message = f"{hello_message}, {name}, {again_message}, {goal_message}\n\n"
            for subject in student.subjects_results:
                message += f"⭐️ {subject.name}\n"
                message += f"Итог: {subject.webinars*100:.0f}% вебов и {subject.homeworks*100:.0f}% домашек\n\n"
            message += f"{advice}\n\n"
            message += random.choice(templates[conclusion_key])

            messages.append(
                f"Трекинг для: {student.student_name}\n\n{message}\n{'-'*50}\n"
            )

        return "\n".join(messages)
