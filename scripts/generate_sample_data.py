import csv
from pathlib import Path


def generate(path: Path, n_students: int, n_questions: int = 2) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "question_id", "answer_text"])
        writer.writeheader()
        for student in range(1, n_students + 1):
            sid = f"S{student:03d}"
            for q in range(1, n_questions + 1):
                writer.writerow(
                    {
                        "student_id": sid,
                        "question_id": f"Q{q}",
                        "answer_text": f"Answer from {sid} for question {q}",
                    }
                )


if __name__ == "__main__":
    base = Path("data/samples")
    base.mkdir(parents=True, exist_ok=True)
    generate(base / "100_students.csv", 100)
    generate(base / "500_students.csv", 500)
    generate(base / "1000_students.csv", 1000)
