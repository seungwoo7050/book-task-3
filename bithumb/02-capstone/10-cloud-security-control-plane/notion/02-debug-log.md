# 디버그 로그

## 실제로 자주 막히는 지점

- archive 문서에는 예전 패키지명과 DB 이름이 남아 있습니다. 현재 코드는 `cloud_security_control_plane` 패키지와 `study2_control_plane` 기본 DB를 기준으로 읽어야 합니다.
- `/v1/scans`로 job을 만든 뒤 `/v1/workers/scans/run`을 호출해야 pending scan이 실제 findings로 바뀝니다. API 요청만으로는 끝나지 않습니다.
- `make demo-capstone`은 Docker가 있으면 PostgreSQL, 없으면 SQLite fallback으로 동작합니다. 이 분기를 문서에서 빼먹으면 재현이 막힙니다.

## 이미 확인된 테스트 시나리오

- `test_control_plane_end_to_end`: Terraform scan job 생성, IAM scan job 생성, worker 실행, CloudTrail/K8s ingestion, exception 승인, remediation dry-run, report 생성까지 한 번에 확인합니다.
- 같은 테스트에서 lake Parquet 생성도 함께 검증합니다.

## 다시 검증할 명령

```bash
make test-capstone
make demo-capstone
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_api.py](../python/tests/test_api.py)
- 앱 진입점: [../python/src/cloud_security_control_plane/app.py](../python/src/cloud_security_control_plane/app.py)
- 데모 설명: [../docs/demo-walkthrough.md](../docs/demo-walkthrough.md)
- 이전 설명: [../notion-archive/essay.md](../notion-archive/essay.md)
