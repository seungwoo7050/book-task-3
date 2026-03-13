# K-distributed-ops-lab Structure Plan

## 한 줄 약속
- 여러 서비스가 함께 살아 있을 때, health와 metrics 질문도 분산시키기

## 독자 질문
- gateway와 내부 서비스가 동시에 존재할 때, 운영성 surface는 어디서부터 service-local이고 어디서부터 system-level인가.
- 서비스별 readiness는 무엇을 확인해야 하는가 request id와 metrics는 어떤 운영 질문에 답하는가 target shape 문서는 어디까지 사실이고 어디부터 가정인가 gateway health와 내부 서비스 health를 왜 같은 의미로 보면 안 되는가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. MSA 실행 뒤 남는 운영 질문을 별도 랩으로 떼기
2. 서비스별 health/metrics와 gateway health를 다른 질문으로 보기
3. system test와 compose health matrix로 운영 surface를 고정하기
4. 2026-03-10 재검증으로 분산 운영성 기준을 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/routes/ops.py::metrics` — service label이 붙은 metrics line으로 분산 운영성 최소 surface를 보여 준다.
- 보조 앵커: `labs/K-distributed-ops-lab/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery` — 분산 runtime이 실제 협업 흐름과 장애 복구를 얼마나 견디는지 보여 주는 최종 smoke다.
- 문서 앵커: `labs/K-distributed-ops-lab/problem/README.md`, `labs/K-distributed-ops-lab/docs/README.md`
- CLI 앵커:
- `make test`
- `make smoke`
- `docker compose up --build`

## 글에서 강조할 개념
- 분산 구조에서 health endpoint가 늘어나는 이유 JSON 로그와 metrics의 최소 기준 Compose health matrix와 AWS 문서의 역할 왜 운영성 문서도 학습 저장소의 핵심 산출물인지
- 서비스별 live / ready request id가 포함된 JSON 로그 최소 metrics surface 실제 클라우드 배포 자동화와 IaC는 제외합니다. trace backend와 log shipping은 붙이지 않습니다.

## 끝맺음
- 제외 범위: 실제 클라우드 배포 자동화 trace backend log shipping
- 검증 문장: 2026-03-10에 gateway/identity/workspace/notification unit test, system test, smoke가 통과했다.
