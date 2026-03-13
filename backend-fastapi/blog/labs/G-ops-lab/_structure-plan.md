# G-ops-lab Structure Plan

## 한 줄 약속
- 기능보다 먼저, 앱이 살아 있고 준비됐다는 질문을 분리하기

## 독자 질문
- 학습용 백엔드에서도 liveness, readiness, metrics, CI, target shape 문서를 어디까지 분리해서 보여줘야 하는가.
- liveness와 readiness는 왜 분리해야 하는가 "최소 metrics"는 어떤 운영 질문에 답해야 하는가 배포 문서는 어디까지 사실이고 어디부터 가정인가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 운영성을 기능 뒤에 숨기지 않고 별도 랩으로 떼기
2. live/ready와 metrics를 별도 route로 굳히기
3. 테스트와 workflow로 운영 surface를 닫기
4. 2026-03-09 재검증으로 문서와 실행을 맞추기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py::metrics` — 최소 metrics가 어떤 운영 질문에 답하는지 가장 직접적으로 드러낸다.
- 보조 앵커: `labs/G-ops-lab/fastapi/tests/integration/test_ops.py::test_live_ready_and_metrics` — live, ready, metrics 세 surface가 함께 검증되는 최소 회귀선이다.
- 문서 앵커: `labs/G-ops-lab/problem/README.md`, `labs/G-ops-lab/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- health endpoint 설계 기준 CI와 로컬 Compose 검증의 역할 차이 AWS target shape 문서를 읽는 방법
- liveness와 readiness의 구분 구조화 로그 최소 metrics endpoint observability stack 전체를 붙이지 않고 최소 surface만 남깁니다. AWS는 실제 배포 자동화가 아니라 문서 수준 target shape로 설명합니다.

## 끝맺음
- 제외 범위: 풀 observability stack 구축 IaC로 실제 인프라를 생성하는 자동화 장시간 부하 테스트와 장애 주입 실험
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다.
