from python.metrics.collector import compute_speedup
from python.preprocessing.parser import load_answers


def test_load_answers_groups_by_question(tmp_path):
    csv_file = tmp_path / "answers.csv"
    csv_file.write_text(
        "student_id,question_id,answer_text\n"
        "S001,Q1,Alpha\n"
        "S002,Q1,Beta\n"
        "S001,Q2,Gamma\n",
        encoding="utf-8",
    )

    grouped = load_answers(str(csv_file))

    assert sorted(grouped.keys()) == ["Q1", "Q2"]
    assert len(grouped["Q1"]) == 2
    assert grouped["Q2"][0].answer_text == "Gamma"


def test_compute_speedup_handles_basic_cases():
    assert compute_speedup(100.0, 50.0) == 2.0
    assert compute_speedup(100.0, 0.0) == 0.0
