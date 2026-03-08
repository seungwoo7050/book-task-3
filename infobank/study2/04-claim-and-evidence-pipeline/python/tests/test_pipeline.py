from stage04.pipeline import extract_claims, verify_claims


def test_claim_pipeline_keeps_retrieval_trace():
    claims = extract_claims('환불은 본인확인 후 접수 가능합니다. 상담원 연결이 필요할 수 있습니다.')
    kb = {'refund_policy.md': '환불은 본인확인 후 접수 가능합니다.'}
    result = verify_claims(claims, kb)
    assert result['claim_results'][0]['verdict'] == 'support'
    assert result['claim_results'][0]['retrieval_trace']['docs'] == ['refund_policy.md']
