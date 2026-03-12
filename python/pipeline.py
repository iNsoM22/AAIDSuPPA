from python.bridge.engine import Engine
from python.embeddings.generator import EmbeddingGenerator
from python.preprocessing.parser import load_answers


def run_analysis(csv_path: str, mode: str, engine_config: dict) -> dict:
    answers_by_question = load_answers(csv_path)

    generator = EmbeddingGenerator()
    engine = Engine()
    all_flagged = []
    all_metrics = {}

    for qid, answers in answers_by_question.items():
        texts = [a.answer_text for a in answers]
        student_ids = [a.student_id for a in answers]

        embeddings = generator.generate(texts)
        result = engine.run(embeddings, mode, engine_config)

        flagged = []
        for pair in result["flagged_pairs"]:
            flagged.append(
                {
                    "student_a": student_ids[pair["i"]],
                    "student_b": student_ids[pair["j"]],
                    "question_id": qid,
                    "score": round(pair["score"], 4),
                }
            )

        all_flagged.extend(flagged)
        all_metrics[qid] = {
            "elapsed_ms": result["elapsed_ms"],
            "n_students": result["n_students"],
            "total_pairs": result["total_pairs"],
            "flagged_pairs": len(flagged),
            "mode": mode,
        }

    return {
        "flagged_pairs": all_flagged,
        "metrics": all_metrics,
        "mode": mode,
    }
