from stage05.judge import judge_response, merge_score


def test_judge_and_score_merge():
    judgment = judge_response('환불 안내', '환불 정책을 확인해 안내드리겠습니다.', [])
    total = merge_score(judgment, groundedness=90.0, compliance=100.0)
    assert total > 85
    assert judgment['failure_types'] == []
