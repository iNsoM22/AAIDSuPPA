import json
import os
import struct
import subprocess
import tempfile

import numpy as np

from python.utils.config import load_config


class EngineError(Exception):
    pass


class Engine:
    def __init__(self):
        cfg = load_config()
        self.binary = cfg["engine"]["binary_path"]
        self.timeout = cfg["engine"]["timeout_seconds"]

    def _write_embeddings(self, embeddings: np.ndarray) -> str:
        n, d = embeddings.shape
        tmp = tempfile.NamedTemporaryFile(suffix=".bin", delete=False)
        tmp.write(struct.pack("II", n, d))
        tmp.write(embeddings.astype(np.float32).tobytes())
        tmp.close()
        return tmp.name

    def run(self, embeddings: np.ndarray, mode: str, config: dict) -> dict:
        input_path = self._write_embeddings(embeddings)
        try:
            cmd = [
                self.binary,
                "--mode",
                mode,
                "--input",
                input_path,
                "--threshold",
                str(config.get("threshold", 0.85)),
                "--threads",
                str(config.get("num_threads", 0)),
                "--schedule",
                config.get("schedule", "dynamic"),
                "--chunk",
                str(config.get("chunk_size", 32)),
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
            if result.returncode != 0:
                raise EngineError(f"Engine error:\n{result.stderr}")
            return json.loads(result.stdout)
        finally:
            os.unlink(input_path)
