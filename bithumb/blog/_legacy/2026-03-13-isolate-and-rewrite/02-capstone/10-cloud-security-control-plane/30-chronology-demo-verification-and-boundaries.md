# 30 Demo, Verification, And Boundaries

이 문서는 capstone의 end-to-end 검증과 demo 산출물을 현재 테스트와 `demo_capture.py`만으로 다시 읽은 기록입니다.

## Day 3
### Session 1

- 목표: 이 캡스톤이 실제로 어느 범위까지 end-to-end를 검증하는지 `test_api.py`와 `demo_capture.py`로 확인한다.
- 진행: 테스트 파일과 demo capture 스크립트를 같이 읽어 scan request -> worker -> ingestion -> exception -> remediation -> report 순서를 따라갔다.
- 이슈: 처음엔 scan worker까지만 연결돼 있을 거라고 생각했는데, 테스트는 exception suppression과 remediation dry-run, report 생성까지 한 번에 묶고 있었다.
- 판단: 이 capstone의 검증 단위는 단순히 “finding이 생기는가”가 아니라, 여러 입력이 한 상태 저장소와 report 계층으로 수렴하는지 확인하는 데 있다.

CLI:

```bash
$ sed -n '1,240p' 02-capstone/10-cloud-security-control-plane/python/tests/test_api.py
$ sed -n '1,260p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/demo_capture.py
```

이 시점의 핵심 코드는 demo가 실제 HTTP 호출 순서로 산출물을 남기는 부분이었다.

```python
    scan_responses.append(client.post("/v1/scans", json={"source": "terraform-plan", "path": str(data_dir / "insecure_plan.json")}).json())
    scan_responses.append(client.post("/v1/scans", json={"source": "iam-policy", "path": str(data_dir / "broad_admin_policy.json")}).json())
    worker_response = client.post("/v1/workers/scans/run").json()
    cloudtrail_response = client.post("/v1/ingestions/cloudtrail", json={"path": str(data_dir / "cloudtrail_suspicious.json")}).json()
    k8s_response = client.post("/v1/ingestions/k8s", json={"path": str(data_dir / "insecure_k8s.yaml")}).json()
```

처음엔 demo가 테스트용 fixture 덤프일 뿐이라고 생각했지만, 실제로는 사용자가 따라가기 쉬운 순서로 API 결과를 파일화해 두는 재현 가이드 역할을 한다. 이 조각 덕분에 README의 “demo 가능”이 실제 산출물 경로와 연결된다.

### Session 2

- 진행: `make test-capstone`, `make demo-capstone`, 생성된 report를 다시 확인했다.
- 검증: `make test-capstone`은 1개 end-to-end 테스트를 통과했고, `make demo-capstone`은 PostgreSQL 컨테이너를 띄운 뒤 `.artifacts/capstone/demo`에 JSON과 Markdown 산출물을 남겼다.
- 판단: 처음 가설은 Docker가 없으면 demo가 막힐 거라는 쪽이었지만, `Makefile`과 `README`를 같이 보면 SQLite fallback 경로까지 고려하고 있어 local reproducibility를 더 우선한다.
- 다음: 여기서 의도적으로 비워 둔 것은 실제 AWS 연동, 외부 큐, 운영용 인증, 멀티테넌시다. 즉 이 프로젝트는 “작동하는 local control plane”까지를 목표로 하고, production platform이라고 주장하지 않는다.

CLI:

```bash
$ make test-capstone
$ make demo-capstone
$ sed -n '1,160p' 02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo/08-report.md
$ sed -n '1,160p' 02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo/07-remediation.json
```

출력:

```text
1 passed in 0.81s
demo assets written to /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo
## Findings
## Remediation Plans
```
