from pathlib import Path
from typing import Any, Dict

import yaml


_DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "configs" / "default.yaml"


def load_config(path: str | None = None) -> Dict[str, Any]:
    cfg_path = Path(path) if path else _DEFAULT_CONFIG
    with cfg_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
