import hashlib
import json
import os
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from python.utils.config import load_config


class EmbeddingGenerator:
    def __init__(self):
        cfg = load_config()
        self.model_name = cfg["embeddings"]["model"]
        self.model = SentenceTransformer(self.model_name)
        self.cache_dir = cfg["embeddings"]["cache_dir"]
        self.batch_size = cfg["embeddings"]["batch_size"]
        os.makedirs(self.cache_dir, exist_ok=True)

    def _cache_key(self, texts: List[str]) -> str:
        payload = {"model": self.model_name, "texts": texts}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{digest}.npy")

    def generate(self, texts: List[str]) -> np.ndarray:
        cache_path = self._cache_key(texts)
        if os.path.exists(cache_path):
            return np.load(cache_path)

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
        )
        np.save(cache_path, embeddings)
        return embeddings
