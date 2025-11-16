from pathlib import Path

from src.tracker_manager import TrackingManager

TABLE = "data.csv"
RESULT = "result.txt"


def main():
    table_path = Path(__file__).parent / TABLE
    result_path = Path(__file__).parent / RESULT

    manager = TrackingManager()
    manager.get_students_results(table_path, result_path)


if __name__ == "__main__":
    main()
