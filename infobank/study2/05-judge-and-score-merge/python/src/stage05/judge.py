def judge_response(user_message: str, assistant_response: str, failures: list[str]) -> dict[str, object]:
    correctness = 90.0 - len(failures) * 10
    resolution = 85.0 if len(assistant_response) > 10 else 70.0
    communication = 85.0 if '안내' in assistant_response or '확인' in assistant_response else 75.0
    return {
        'correctness': max(correctness, 0.0),
        'resolution': resolution,
        'communication': communication,
        'failure_types': sorted(set(failures)),
    }


def merge_score(judgment: dict[str, object], groundedness: float, compliance: float) -> float:
    return round(
        float(judgment['correctness']) * 0.30
        + groundedness * 0.25
        + compliance * 0.20
        + float(judgment['resolution']) * 0.15
        + float(judgment['communication']) * 0.10,
        2,
    )
