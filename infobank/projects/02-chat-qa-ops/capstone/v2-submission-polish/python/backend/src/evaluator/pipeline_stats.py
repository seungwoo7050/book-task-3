from __future__ import annotations

import threading

from core.types import PipelineStats


class _StatsStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self.eval_count = 0
            self.eval_total_ms_sum = 0.0
            self.judge_ms_sum = 0.0
            self.retrieval_hit_sum = 0.0
            self.critical_short_circuit_count = 0
            self.cache_hit_count = 0
            self.version_compare_count = 0
            self.version_compare_ms_sum = 0.0
            self.dependency_fail_count = 0
            self.judge_model = "n/a"
            self.claim_model = "n/a"
            self.evidence_model = "n/a"
            self.retrieval_backend = "n/a"

    def record_eval(
        self,
        *,
        eval_ms: int,
        judge_ms: int,
        retrieval_hit_at_k: float,
        short_circuit: bool,
        judge_model: str,
        claim_model: str,
        evidence_model: str,
        retrieval_backend: str,
    ) -> None:
        with self._lock:
            self.eval_count += 1
            self.eval_total_ms_sum += eval_ms
            self.judge_ms_sum += judge_ms
            self.retrieval_hit_sum += retrieval_hit_at_k
            self.judge_model = judge_model
            self.claim_model = claim_model
            self.evidence_model = evidence_model
            self.retrieval_backend = retrieval_backend
            if short_circuit:
                self.critical_short_circuit_count += 1

    def record_cache_hit(self) -> None:
        with self._lock:
            self.cache_hit_count += 1

    def record_version_compare(self, elapsed_ms: int) -> None:
        with self._lock:
            self.version_compare_count += 1
            self.version_compare_ms_sum += elapsed_ms

    def record_dependency_failure(self) -> None:
        with self._lock:
            self.dependency_fail_count += 1

    def snapshot(self) -> PipelineStats:
        with self._lock:
            eval_count = max(self.eval_count, 1)
            compare_count = max(self.version_compare_count, 1)
            return PipelineStats(
                eval_count=self.eval_count,
                eval_total_ms_avg=round(self.eval_total_ms_sum / eval_count, 2),
                judge_ms_avg=round(self.judge_ms_sum / eval_count, 2),
                retrieval_hit_at_k=round(self.retrieval_hit_sum / eval_count, 4),
                critical_short_circuit_rate=round(self.critical_short_circuit_count / eval_count, 4),
                cache_hit_rate=round(self.cache_hit_count / eval_count, 4),
                version_compare_job_ms_avg=round(self.version_compare_ms_sum / compare_count, 2),
                judge_model=self.judge_model,
                claim_model=self.claim_model,
                evidence_model=self.evidence_model,
                retrieval_backend=self.retrieval_backend,
                dependency_fail_count=self.dependency_fail_count,
            )


_STATS = _StatsStore()


def get_stats_store() -> _StatsStore:
    return _STATS


def reset_stats_store() -> None:
    _STATS.reset()
