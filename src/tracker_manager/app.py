from pathlib import Path
from ..infrastructure import TrackingFactory


class TrackingManager:
    def __init__(self):
        self.tracking_factory = TrackingFactory()

    def get_students_results(self, table_path: Path, save_path: Path) -> None:
        message = self.tracking_factory.get_results(table_path)
        with open(save_path, "w", encoding="utf=8") as file:
            file.write(message)
