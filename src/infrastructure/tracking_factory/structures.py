from dataclasses import dataclass


@dataclass
class subject_result:
    name: str
    webinars: float
    homeworks: float


@dataclass
class student_result:
    student_name: str
    subjects_results: list[subject_result]
