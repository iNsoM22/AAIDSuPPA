from dataclasses import dataclass


@dataclass
class RunMetric:
    mode: str
    elapsed_ms: float
    total_pairs: int

    @property
    def pairs_per_second(self) -> float:
        if self.elapsed_ms <= 0:
            return 0.0
        return (self.total_pairs * 1000.0) / self.elapsed_ms


def compute_speedup(serial_ms: float, omp_ms: float) -> float:
    if omp_ms <= 0:
        return 0.0
    return serial_ms / omp_ms
