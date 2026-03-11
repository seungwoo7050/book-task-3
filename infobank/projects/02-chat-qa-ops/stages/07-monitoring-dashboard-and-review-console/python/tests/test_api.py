from fastapi.testclient import TestClient

from stage07.app import app


client = TestClient(app)


def test_dashboard_snapshot_endpoints():
    assert client.get('/api/dashboard/overview').status_code == 200
    assert client.get('/api/dashboard/failures').json()['items'][0]['failure_type'] == 'MISSING_REQUIRED_EVIDENCE_DOC'
    assert client.get('/api/conversations/conv-001').json()['turns'][0]['evaluation']['lineage']['run_label'] == 'v1.1'
    assert client.post('/api/golden-set/run').json()['avg_score'] == 87.76
    assert client.get('/api/dashboard/version-compare').json()['result']['delta'] == 3.7
