from stage01.rubric import WEIGHTS, merge_score


def test_weights_sum_to_one():
    assert round(sum(WEIGHTS.values()), 5) == 1.0


def test_critical_override_wins():
    result = merge_score(correctness=100, groundedness=100, compliance=100, resolution=100, communication=100, critical=True)
    assert result == {"total": 0.0, "grade": "CRITICAL"}


def test_grade_band_contract():
    result = merge_score(correctness=90, groundedness=90, compliance=90, resolution=90, communication=90, critical=False)
    assert result["grade"] == "A"
