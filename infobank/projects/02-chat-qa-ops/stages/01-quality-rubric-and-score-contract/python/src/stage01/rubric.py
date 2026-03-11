WEIGHTS = {
    "correctness": 0.30,
    "groundedness": 0.25,
    "compliance": 0.20,
    "resolution": 0.15,
    "communication": 0.10,
}
GRADE_BANDS = (("A", 90), ("B", 75), ("C", 60), ("D", 40))


def to_grade(total: float) -> str:
    for grade, minimum in GRADE_BANDS:
        if total >= minimum:
            return grade
    return "F"


def merge_score(*, correctness: float, groundedness: float, compliance: float, resolution: float, communication: float, critical: bool) -> dict[str, object]:
    if critical:
        return {"total": 0.0, "grade": "CRITICAL"}
    total = (
        correctness * WEIGHTS["correctness"]
        + groundedness * WEIGHTS["groundedness"]
        + compliance * WEIGHTS["compliance"]
        + resolution * WEIGHTS["resolution"]
        + communication * WEIGHTS["communication"]
    )
    total = round(total, 2)
    return {"total": total, "grade": to_grade(total)}
