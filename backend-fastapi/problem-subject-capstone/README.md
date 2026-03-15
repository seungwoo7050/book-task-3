# backend-fastapi 서버 캡스톤 문제지

`backend-fastapi`의 capstone은 개별 랩에서 분리해 연습한 인증, 인가, 데이터 API, 비동기 전달, 운영성 문제를 하나의 협업형 백엔드로 다시 조합하게 만드는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [workspace-backend-fastapi](workspace-backend-fastapi.md) | 시작 위치의 구현을 완성해 로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명 가능해야 합니다, 워크스페이스 멤버십과 역할이 프로젝트/태스크/댓글 API와 연결되어야 합니다, 알림 생성이 큐와 실시간 전달로 이어지는 흐름이 보여야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend/fastapi && PYTHONPATH=. python3 -m pytest` |
| [workspace-backend-v2-msa-fastapi](workspace-backend-v2-msa-fastapi.md) | 시작 위치의 구현을 완성해 gateway가 public /api/v1/auth/*, /api/v1/platform/* 경로를 유지해야 한다, identity-service, workspace-service, notification-service는 각자 자기 DB만 읽어야 한다, 댓글 생성은 outbox에 기록되고, 이후 stream consumer와 websocket fan-out으로 이어져야 한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/gateway test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
