# backend-fastapi 서버 캡스톤 답안지

이 문서는 FastAPI 트랙의 capstone 두 개를 실제 통합 구현 기준으로 정리한 답안지다. 첫 번째 capstone은 인증, 협업 도메인, 알림, 실시간 전달을 단일 서비스 안에서 끝까지 묶는 기준선이고, 두 번째 capstone은 같은 도메인을 gateway와 내부 서비스들로 다시 나눠 public contract와 내부 분산 복잡성을 동시에 다룬다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [workspace-backend-fastapi](workspace-backend-fastapi_answer.md) | 시작 위치의 구현을 완성해 로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명 가능해야 합니다, 워크스페이스 멤버십과 역할이 프로젝트/태스크/댓글 API와 연결되어야 합니다, 알림 생성이 큐와 실시간 전달로 이어지는 흐름이 보여야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 get_auth_service와 get_mailbox, require_csrf 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend/fastapi && PYTHONPATH=. python3 -m pytest` |
| [workspace-backend-v2-msa-fastapi](workspace-backend-v2-msa-fastapi_answer.md) | 시작 위치의 구현을 완성해 gateway가 public /api/v1/auth/*, /api/v1/platform/* 경로를 유지해야 한다, identity-service, workspace-service, notification-service는 각자 자기 DB만 읽어야 한다, 댓글 생성은 outbox에 기록되고, 이후 stream consumer와 websocket fan-out으로 이어져야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 get_service_client와 get_current_claims, require_csrf 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
