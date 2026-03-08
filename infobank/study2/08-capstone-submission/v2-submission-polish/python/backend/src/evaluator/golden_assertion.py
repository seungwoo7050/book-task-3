from __future__ import annotations

from core.types import GoldenAssertionResult, GoldenCaseAssertion


def _collect_evidence_doc_ids(evaluation: dict[str, object], retrieved_doc_ids: list[str]) -> set[str]:
    collected = {doc_id for doc_id in retrieved_doc_ids if isinstance(doc_id, str)}
    evidence_results = evaluation.get("evidence_results", {})
    if not isinstance(evidence_results, dict):
        return collected
    claim_results = evidence_results.get("claim_results", [])
    if not isinstance(claim_results, list):
        return collected
    for claim_result in claim_results:
        if not isinstance(claim_result, dict):
            continue
        evidence_doc_ids = claim_result.get("evidence_doc_ids", [])
        if not isinstance(evidence_doc_ids, list):
            continue
        for item in evidence_doc_ids:
            if isinstance(item, str):
                collected.add(item)
    return collected


def evaluate_golden_case(
    *,
    case_id: str,
    expected_config: dict[str, object],
    evaluation: dict[str, object],
    retrieved_doc_ids: list[str],
) -> GoldenCaseAssertion:
    expected_failure_types_raw = expected_config.get("expected_failure_types", [])
    expected_failure_types_list = expected_failure_types_raw if isinstance(expected_failure_types_raw, list) else []
    expected_failure_types = {str(item) for item in expected_failure_types_list if isinstance(item, str) and item.strip()}
    expected_evidence_doc_ids_raw = expected_config.get("required_evidence_doc_ids", [])
    expected_evidence_doc_ids_list = expected_evidence_doc_ids_raw if isinstance(expected_evidence_doc_ids_raw, list) else []
    expected_evidence_doc_ids = {
        str(item) for item in expected_evidence_doc_ids_list if isinstance(item, str) and item.strip()
    }

    actual_failure_types_raw = evaluation.get("failure_types", [])
    actual_failure_types_list = actual_failure_types_raw if isinstance(actual_failure_types_raw, list) else []
    actual_failure_types = {str(item) for item in actual_failure_types_list if isinstance(item, str) and item.strip()}
    actual_evidence_doc_ids = _collect_evidence_doc_ids(evaluation, retrieved_doc_ids)

    reason_codes: list[str] = []
    failure_passed = expected_failure_types.issubset(actual_failure_types)
    if not failure_passed:
        reason_codes.append("MISSING_EXPECTED_FAILURE_TYPES")

    evidence_passed = True
    if expected_evidence_doc_ids:
        evidence_passed = bool(expected_evidence_doc_ids & actual_evidence_doc_ids)
        if not evidence_passed:
            reason_codes.append("MISSING_REQUIRED_EVIDENCE_DOC")

    return GoldenCaseAssertion(
        case_id=case_id,
        passed=failure_passed and evidence_passed,
        reason_codes=reason_codes,
        expected={
            "expected_failure_types": sorted(expected_failure_types),
            "required_evidence_doc_ids": sorted(expected_evidence_doc_ids),
        },
        actual={
            "failure_types": sorted(actual_failure_types),
            "evidence_doc_ids": sorted(actual_evidence_doc_ids),
        },
    )


def summarize_assertions(assertions: list[GoldenCaseAssertion]) -> GoldenAssertionResult:
    pass_count = sum(1 for item in assertions if item.passed)
    fail_items = [item for item in assertions if not item.passed]
    return GoldenAssertionResult(
        pass_count=pass_count,
        fail_count=len(fail_items),
        assertion_failures=fail_items,
    )
