from __future__ import annotations

import csv
import io

from flask import Blueprint, Response, jsonify

from web.routes.run import get_job

results_bp = Blueprint("results", __name__)


@results_bp.get("/<job_id>")
def results(job_id: str):
    job = get_job(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    if job["status"] != "done":
        return jsonify({"error": "job not complete", "status": job["status"]}), 409

    result = job["result"]
    return jsonify(
        {
            "flagged_pairs": result["flagged_pairs"],
            "metrics": result["metrics"],
            "summary": {
                "total_flagged": len(result["flagged_pairs"]),
                "mode": result["mode"],
            },
        }
    )


@results_bp.get("/<job_id>/download")
def download(job_id: str):
    job = get_job(job_id)
    if not job or job.get("status") != "done":
        return jsonify({"error": "job not complete"}), 409

    result = job["result"]
    rows = result["flagged_pairs"]

    stream = io.StringIO()
    writer = csv.DictWriter(
        stream,
        fieldnames=["student_a", "student_b", "question_id", "score"],
    )
    writer.writeheader()
    writer.writerows(rows)

    return Response(
        stream.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={job_id}_flagged_pairs.csv"},
    )
