# workspace-backend Structure Plan

## 한 줄 초점
- A~G 랩의 개념을 한 FastAPI 앱 안에 다시 묶되, 무엇을 일부러 아직 수동으로 남겨 둔 기준선인지 설명한다.

## 독자 질문
- 인증, 워크스페이스 인가, comment write path, notification delivery를 한 프로세스에 넣으면 무엇이 쉬워지고 무엇이 아직 남는가?
- 왜 이 capstone은 "풀스택 협업 제품"이 아니라 `workspace-backend-v2-msa`와 비교하기 위한 단일 백엔드 기준선인가?

## 본문 구성
1. 문제 정의
   기능 합치기가 아니라 기준선 재조합이라는 점을 잡는다.
2. 인증 조합
   local + Google이 같은 사용자 모델과 같은 session 규약으로 닫히는 구조를 본다.
3. 플랫폼 경계
   workspace membership guard가 project/task/comment write path를 어떻게 지배하는지 본다.
4. comment 이후
   queued notification, manual drain, WebSocket fan-out, presence TTL이 한꺼번에 이어지는 지점을 설명한다.
5. 운영과 한계
   live/ready, Compose 3-service topology, 미연결 rate limiter, 최소 JSON logging을 정리한다.
6. 검증 상태
   lint 통과와 test/smoke 실패 원인을 현재 사실로 닫는다.

## 반드시 연결할 증거
- `fastapi/app/main.py`
  schema auto-create와 app.state runtime 구성
- `fastapi/app/domain/services/auth.py`
  local + Google + refresh token family rotation
- `fastapi/app/domain/services/platform.py`
  membership guard, queued notification, manual drain
- `fastapi/app/runtime.py`
  memory connection manager, presence TTL
- `fastapi/tests/integration/test_capstone.py`
  owner/collaborator 통합 시나리오

## 서술 원칙
- 기존 blog 문장을 입력으로 삼지 않는다.
- "랩을 합쳤다"는 요약보다, 어떤 단순화를 의도적으로 유지했는지를 강조한다.
- 보안/운영 완성도를 과장하지 않는다.
- 현재 재실행 결과의 실패도 본문에 넣는다.

## 이번 턴의 결론 문장
- `workspace-backend`는 모든 것을 끝낸 제품이 아니라, 단일 앱으로 묶었을 때의 단순함과 수동 seam을 보존한 기준선이다.
