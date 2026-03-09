from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Metrics:
    counters: dict[str, int] = field(
        default_factory=lambda: {
            "scan_jobs_created_total": 0,
            "scan_jobs_processed_total": 0,
            "findings_created_total": 0,
            "cloudtrail_ingestions_total": 0,
            "k8s_ingestions_total": 0,
            "remediation_requests_total": 0,
        }
    )

    def inc(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount

    def render(self) -> str:
        lines = [f"study2_{name} {value}" for name, value in sorted(self.counters.items())]
        return "\n".join(lines) + "\n"

