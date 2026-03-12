from dataclasses import dataclass
from typing import Dict, List

import pandas as pd


@dataclass
class StudentAnswer:
    student_id: str
    question_id: str
    answer_text: str


def load_answers(filepath: str) -> Dict[str, List[StudentAnswer]]:
    df = pd.read_csv(filepath, dtype=str).fillna("")
    answers_by_question: Dict[str, List[StudentAnswer]] = {}

    for _, row in df.iterrows():
        ans = StudentAnswer(
            student_id=row["student_id"].strip(),
            question_id=row["question_id"].strip(),
            answer_text=row["answer_text"].strip(),
        )
        answers_by_question.setdefault(ans.question_id, []).append(ans)

    return answers_by_question
