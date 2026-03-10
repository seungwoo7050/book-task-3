# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- control plane은 스캐너 모음이 아니라 요청, 처리, 저장, 예외, 조치, 보고를 잇는 운영 흐름입니다.
- API와 worker 분리는 느린 처리와 즉시 응답을 분리하는 기본 구조입니다.
- PostgreSQL 기본 + SQLite fallback은 학습용 로컬 재현성을 크게 높입니다.
- end-to-end 테스트와 데모 산출물은 README 설명보다 강한 통합 근거입니다.

## 로컬 근거 파일

- 아키텍처 요약: [../docs/concepts/architecture.md](../docs/concepts/architecture.md)
- 데모 설명: [../docs/demo-walkthrough.md](../docs/demo-walkthrough.md)
- 앱 진입점: [../python/src/cloud_security_control_plane/app.py](../python/src/cloud_security_control_plane/app.py)
- CLI 진입점: [../python/src/cloud_security_control_plane/cli.py](../python/src/cloud_security_control_plane/cli.py)
- 데모 캡처 스크립트: [../python/src/cloud_security_control_plane/demo_capture.py](../python/src/cloud_security_control_plane/demo_capture.py)
- 통합 검증: [../python/tests/test_api.py](../python/tests/test_api.py)

## 재현 체크포인트

- scan worker가 pending job 2개를 처리하는지 확인합니다.
- CloudTrail과 K8s ingestion 이후 findings가 6건 이상 누적되는지 확인합니다.
- exception 적용 후 finding 하나가 `suppressed` 상태로 바뀌는지 확인합니다.
- 최종 report에 `## Findings`, `## Exceptions`, `## Remediation Plans`가 모두 포함되는지 확인합니다.

## 다음 프로젝트로 이어지는 질문

- 이 프로젝트는 앞선 01~09를 통합한 종착점이지만, 동시에 이후에는 실제 인증, 큐, 운영 관찰성으로 확장할 수 있는 출발점이기도 합니다.
- 학습자는 여기서 “서비스를 하나 만들었다”보다 “어떤 작은 엔진들을 조합했는가”를 먼저 설명할 수 있어야 합니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
