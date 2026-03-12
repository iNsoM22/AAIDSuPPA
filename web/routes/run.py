from __future__ import annotations

import threading
import time
import uuid

from flask import Blueprint, jsonify, request

from web.routes.upload import get_upload_path

run_bp = Blueprint("run", __name__)

_JOBS: dict[str, dict] = {}


def _runner(job_id: str, upload_id: str, mode: str, config: dict):
    _JOBS[job_id]["status"] = "running"
    _JOBS[job_id]["progress"] = 20
    time.sleep(0.01)

    try:
        csv_path = get_upload_path(upload_id)
        if not csv_path:
            raise ValueError("invalid upload_id")

        _JOBS[job_id]["progress"] = 60
        from python.pipeline import run_analysis

        result = run_analysis(csv_path, mode, config)
        _JOBS[job_id]["result"] = result
        _JOBS[job_id]["status"] = "done"
        _JOBS[job_id]["progress"] = 100
    except Exception as exc:
        _JOBS[job_id]["status"] = "error"
        _JOBS[job_id]["error"] = str(exc)


@run_bp.post("/analyze")
def analyze():
    body = request.get_json(silent=True) or {}
    upload_id = body.get("upload_id", "")
    mode = body.get("mode", "serial")

    config = {
        "threshold": body.get("threshold", 0.85),
        "num_threads": body.get("num_threads", 0),
        "schedule": body.get("schedule", "dynamic"),
        "chunk_size": body.get("chunk_size", 32),
    }

    if mode not in {"serial", "omp"}:
        return jsonify({"error": "mode must be serial or omp"}), 400

    job_id = str(uuid.uuid4())
    _JOBS[job_id] = {"status": "pending", "progress": 0, "upload_id": upload_id}

    thread = threading.Thread(target=_runner, args=(job_id, upload_id, mode, config), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id})


@run_bp.get("/status/<job_id>")
def status(job_id: str):
    job = _JOBS.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404

    payload = {"status": job["status"], "progress": job["progress"]}
    if job["status"] == "error":
        payload["error"] = job.get("error", "unknown")
    return jsonify(payload)


def get_job(job_id: str) -> dict | None:
    return _JOBS.get(job_id)
