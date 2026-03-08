from fastapi import FastAPI

app = FastAPI()

SNAPSHOT = {
    'overview': {'avg_score': 87.76, 'fail_rate': 0.0, 'critical_count': 0, 'evaluation_count': 30, 'avg_latency_ms': 112.4, 'grade_distribution': {'A': 19, 'B': 11}, 'failure_top': [], 'run_labels': ['v1.0', 'v1.1']},
    'failures': {'items': [{'failure_type': 'MISSING_REQUIRED_EVIDENCE_DOC', 'count': 11, 'critical_count': 0, 'avg_score': 66.0}]},
    'conversations': {'items': [{'id': 'conv-001', 'created_at': '2026-03-07T00:00:00+00:00', 'prompt_version': 'v1.0', 'kb_version': 'v1.1', 'run_id': 'run-001', 'turn_count': 1, 'session_score': 90.0, 'session_grade': 'A'}]},
    'conversation_detail': {'conversation': {'id': 'conv-001', 'created_at': '2026-03-07T00:00:00+00:00', 'prompt_version': 'v1.0', 'kb_version': 'v1.1', 'run_id': 'run-001', 'turn_count': 1, 'session_score': 90.0, 'session_grade': 'A'}, 'turns': [{'id': 'turn-001', 'turn_index': 1, 'user_message': '환불 접수 전에 인증 필수인가요?', 'assistant_response': '환불은 본인확인 후 접수 가능하며, 인증 실패 시 상담원 연결 후 추가 확인 절차를 진행합니다.', 'retrieved_doc_ids': ['refund_policy.md', 'identity_verification.md'], 'evaluation': {'id': 'eval-001', 'grade': 'A', 'total_score': 90.0, 'failure_types': [], 'lineage': {'run_label': 'v1.1', 'dataset': 'golden-set', 'trace_id': 'trace-001', 'retrieval_version': 'retrieval-v2'}, 'judge_trace': {'provider': 'heuristic', 'model': 'judge-v2', 'short_circuit': False, 'short_circuit_reason': None}}}]},
    'golden_run': {'run_id': 'run-001', 'run_label': 'v1.1', 'dataset': 'golden-set', 'count': 30, 'avg_score': 87.76, 'critical_count': 0, 'pass_count': 19, 'fail_count': 11},
    'compare': {'result': {'baseline': 'v1.0', 'candidate': 'v1.1', 'dataset': 'golden-set', 'baseline_avg': 84.06, 'candidate_avg': 87.76, 'baseline_critical': 2, 'candidate_critical': 0, 'baseline_pass_count': 16, 'candidate_pass_count': 19, 'baseline_fail_count': 14, 'candidate_fail_count': 11, 'baseline_failures': {'MISSING_REQUIRED_EVIDENCE_DOC': 14}, 'candidate_failures': {'MISSING_REQUIRED_EVIDENCE_DOC': 11}, 'delta': 3.7, 'pass_delta': 3, 'fail_delta': -3, 'critical_delta': -2}},
}


@app.get('/api/dashboard/overview')
def overview() -> dict[str, object]:
    return SNAPSHOT['overview']


@app.get('/api/dashboard/failures')
def failures() -> dict[str, object]:
    return SNAPSHOT['failures']


@app.get('/api/conversations')
def conversations() -> dict[str, object]:
    return SNAPSHOT['conversations']


@app.get('/api/conversations/{conversation_id}')
def conversation_detail(conversation_id: str) -> dict[str, object]:
    assert conversation_id == 'conv-001'
    return SNAPSHOT['conversation_detail']


@app.post('/api/golden-set/run')
def golden_run() -> dict[str, object]:
    return SNAPSHOT['golden_run']


@app.get('/api/dashboard/version-compare')
def version_compare() -> dict[str, object]:
    return SNAPSHOT['compare']
