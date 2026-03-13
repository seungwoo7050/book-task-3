# 10 Inputs And API Surface

이 문서는 capstone의 공개 표면과 입력 경계를 현재 FastAPI app, CLI, 테스트만으로 다시 읽은 기록입니다.

## Day 1
### Session 1

- 목표: 이 캡스톤의 첫 공개 표면이 CLI인지 API인지, 그리고 어떤 입력 소스를 어디서 받는지 확인한다.
- 진행: `README.md`, `problem/README.md`, `python/README.md`, `docs/concepts/architecture.md`, `app.py`, `test_api.py`를 차례대로 읽었다.
- 이슈: 처음엔 CLI가 주 진입점이라고 생각했는데, 실제 코드와 테스트를 보니 public boundary는 `FastAPI create_app()`와 route 집합이었다.
- 판단: CLI는 디버그용 보조 표면이고, 프로젝트 설명의 중심은 `/v1/scans`, `/v1/ingestions/*`, `/v1/findings`, `/v1/exceptions`, `/v1/remediations/*`, `/v1/reports/latest` 같은 HTTP 경계에 둬야 자연스럽다.

CLI:

```bash
$ sed -n '1,160p' 02-capstone/10-cloud-security-control-plane/README.md
$ sed -n '1,200p' 02-capstone/10-cloud-security-control-plane/problem/README.md
$ sed -n '1,260p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/app.py
$ sed -n '1,220p' 02-capstone/10-cloud-security-control-plane/python/tests/test_api.py
```

이 시점의 핵심 코드는 scan 요청을 job으로 끊고, 오래 걸리는 처리를 worker로 넘기는 API였다.

```python
    @app.post("/v1/scans")
    def create_scan(payload: ScanRequest) -> dict[str, str]:
        with app.state.session_factory() as session:
            job = db.create_scan_job(session, payload.source, payload.path)
            session.commit()
        app.state.metrics.inc("scan_jobs_created_total")
        return {"id": job.id, "status": job.status}
```

처음엔 스캔을 요청하면 바로 finding을 돌려주는 구조일 거라고 생각했지만, 나중에 보니 이 capstone은 API 응답과 실제 스캔을 분리해 `scan_jobs` 상태 전이를 먼저 보여 주는 쪽을 택했다. 이 선택 덕분에 worker 모델과 metrics 설명이 훨씬 쉬워진다.

### Session 2

- 진행: `workers.py`, `scanners.py`, CLI scan 명령을 같이 읽어 어떤 입력이 어느 스캐너로 연결되는지 확인했다.
- 검증: CLI `scan terraform-plan`은 현재 insecure plan에서 3개 finding을 반환했다.
- 판단: 처음 가설은 capstone이 앞선 프로젝트 코드를 import해서 그대로 감쌀 것이라는 쪽이었지만, 실제 구현은 같은 아이디어를 capstone용 `Finding` schema와 ID 생성 규칙으로 다시 옮겨 놓은 얇은 통합층에 가깝다.
- 다음: 입력 경계가 잡혔으니, 다음 단계에서는 findings가 어떤 DB 테이블과 suppression 규칙 위에 저장되는지 봐야 한다.

CLI:

```bash
$ sed -n '1,260p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/workers.py
$ sed -n '1,260p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/scanners.py
$ PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json
```

출력:

```text
"control_id": "CSPM-001"
"control_id": "CSPM-003"
```
