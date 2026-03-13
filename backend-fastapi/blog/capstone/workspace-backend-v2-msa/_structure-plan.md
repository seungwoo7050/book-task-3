# workspace-backend-v2-msa Structure Plan

## 한 줄 약속
- 단일 백엔드 기준선을 MSA로 다시 풀고, 장애 복구까지 public API로 증명하기

## 독자 질문
- v1과 같은 협업형 도메인을 MSA로 다시 풀었을 때 무엇이 단순해지고 무엇이 더 복잡해지는가.
- 왜 `platform`을 그대로 두지 않고 `identity/workspace/notification`으로 나눴는가 public API는 왜 gateway에서 유지하는가 outbox, stream, pub/sub은 각각 어느 경계에 필요한가 v1보다 좋아진 점과 나빠진 점은 무엇인가 무엇이 실제 검증된 사실이고, 무엇이 아직 target shape 문서 수준의 가정인가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. v1 단일 백엔드 기준선을 다시 분해하기
2. gateway와 세 서비스의 runtime scope를 compose로 고정하기
3. system test로 public flow와 recovery를 한 번에 묶기
4. 2026-03-10 재검증과 fresh build 문제를 사실대로 남기기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `capstone/workspace-backend-v2-msa/fastapi/compose.yaml::__compose__` — gateway, identity, workspace, notification, redis가 실제 runtime을 이루는 비교 대상 surface다.
- 보조 앵커: `capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery` — public API, invite, comment, drain failure, recovery, websocket fan-out을 한 흐름으로 담은 핵심 증거다.
- 문서 앵커: `capstone/workspace-backend-v2-msa/problem/README.md`, `capstone/workspace-backend-v2-msa/docs/README.md`
- CLI 앵커:
- `make test (service unit tests)`
- `docker compose up --build -d (재시도)`
- `docker build --progress=plain -t workspace-v2-identity-fresh ./services/identity-service`
- `docker pull python:3.12-slim`
- `docker compose -p workspace-backend-v2-msa-dd63448c -f compose.yaml up -d --no-build`
- `inline Python end-to-end flow for register -> verify -> login -> invite -> comment -> drain -> recovery -> websocket`

## 글에서 강조할 개념
- 브라우저 쿠키와 CSRF가 왜 gateway에만 있어야 하는가 서비스별 DB ownership과 bearer claims 규칙 `comment.created.v1` 흐름과 eventual consistency notification-service 장애가 comment 생성과 분리되어야 하는 이유 운영 문서에서 target shape와 실제 검증 완료를 어떻게 구분해야 하는가
- 브라우저 쿠키와 CSRF는 gateway에만 두고 내부 서비스는 bearer claims만 읽도록 경계를 나눴습니다. 서비스별 DB ownership을 지키고 사용자 정보는 claims와 event payload로만 전달합니다. notification-service 장애가 댓글 생성 성공을 막지 않도록 eventual consistency를 전제로 설계했습니다.

## 끝맺음
- 제외 범위: Kubernetes, service mesh, service discovery 실제 클라우드 배포 자동화와 IaC front-end 렌더링과 정적 자산 saga orchestration과 다단계 보상 흐름
- 검증 문장: 2026-03-10에 service unit tests는 통과했고, fresh build 경로는 Docker Desktop 문제로 성공 기록을 남기지 못했지만 prebuilt image 기준 Compose runtime과 end-to-end 협업 흐름 검증은 완료했다.
