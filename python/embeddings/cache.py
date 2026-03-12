from pathlib import Path


def clear_cache(cache_dir: str) -> int:
    removed = 0
    for path in Path(cache_dir).glob("*.npy"):
        path.unlink()
        removed += 1
    return removed
