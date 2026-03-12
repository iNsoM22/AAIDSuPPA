from __future__ import annotations

import csv
import uuid
from pathlib import Path

from flask import Blueprint, jsonify, request

upload_bp = Blueprint("upload", __name__)

_UPLOAD_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"
_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
_UPLOADS: dict[str, str] = {}


def _count_csv(path: Path) -> tuple[int, int]:
    students = set()
    questions = set()
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.add((row.get("student_id") or "").strip())
            questions.add((row.get("question_id") or "").strip())
    students.discard("")
    questions.discard("")
    return len(students), len(questions)


@upload_bp.post("/answers")
def upload_answers():
    file = request.files.get("file")
    if file is None or file.filename == "":
        return jsonify({"error": "file is required"}), 400

    upload_id = str(uuid.uuid4())
    path = _UPLOAD_DIR / f"{upload_id}.csv"
    file.save(path)
    _UPLOADS[upload_id] = str(path)

    n_students, n_questions = _count_csv(path)
    return jsonify(
        {
            "upload_id": upload_id,
            "n_students": n_students,
            "n_questions": n_questions,
        }
    )


def get_upload_path(upload_id: str) -> str | None:
    return _UPLOADS.get(upload_id)
