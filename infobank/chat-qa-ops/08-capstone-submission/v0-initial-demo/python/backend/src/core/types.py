from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RuleResult:
    rule_id: str
    severity: str
    failure_type: str
    matched: bool
    evidence: str = ""
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Claim:
    claim_id: str
    statement: str
    criticality: str
    domain: str
    source_span: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceClaimResult:
    claim_id: str
    verdict: str
    evidence_doc_ids: list[str]
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceResult:
    claim_results: list[EvidenceClaimResult] = field(default_factory=list)
    groundedness_score: float = 0.0
    has_contradiction: bool = False
    retrieval_hit_at_k: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_results": [item.to_dict() for item in self.claim_results],
            "groundedness_score": self.groundedness_score,
            "has_contradiction": self.has_contradiction,
            "retrieval_hit_at_k": self.retrieval_hit_at_k,
        }


@dataclass
class LLMJudgment:
    correctness: float
    resolution: float
    communication: float
    escalation_needed: bool
    failure_types: list[str]
    explanation: str
    judge_ms: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QualityScore:
    total: float
    grade: str
    correctness: float
    groundedness: float
    compliance: float
    resolution: float
    communication: float
    failure_types: list[str]
    is_critical: bool
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VersionCompareResult:
    baseline: str
    candidate: str
    baseline_avg: float
    candidate_avg: float
    baseline_critical: int
    candidate_critical: int
    baseline_forbidden_promise: int
    candidate_forbidden_promise: int
    delta: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DependencyErrorInfo:
    error_code: str
    message: str
    component: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GoldenCaseAssertion:
    case_id: str
    passed: bool
    reason_codes: list[str]
    expected: dict[str, Any]
    actual: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GoldenAssertionResult:
    pass_count: int
    fail_count: int
    assertion_failures: list[GoldenCaseAssertion]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "assertion_failures": [item.to_dict() for item in self.assertion_failures],
        }


@dataclass
class PipelineStats:
    eval_count: int
    eval_total_ms_avg: float
    judge_ms_avg: float
    retrieval_hit_at_k: float
    critical_short_circuit_rate: float
    cache_hit_rate: float
    version_compare_job_ms_avg: float
    judge_model: str
    claim_model: str
    evidence_model: str
    retrieval_backend: str
    dependency_fail_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
