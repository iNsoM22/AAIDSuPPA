from pathlib import Path


REQUIRED_COLUMNS = {"student_id", "question_id", "answer_text"}


def validate_csv_path(path: str) -> None:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise ValueError(f"Input file does not exist: {path}")
    if p.suffix.lower() != ".csv":
        raise ValueError("Only CSV uploads are supported")
