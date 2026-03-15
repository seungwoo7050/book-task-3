# backend-fastapi 서버 개발 비필수 문제지

여기서 `비필수`는 FastAPI 학습 가치가 낮다는 뜻이 아니라, 서버 공통 필수보다 제품형 협업 API 문맥 의존성이 더 강하다는 뜻입니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [a-auth-lab-fastapi](a-auth-lab-fastapi.md) | 시작 위치의 구현을 완성해 회원가입과 로그인 흐름이 분리되어 설명 가능해야 합니다, 이메일 검증과 비밀번호 재설정 토큰 발급/소비가 동작해야 합니다, refresh token rotation이 왜 필요한지 코드와 문서로 설명할 수 있어야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi && PYTHONPATH=. python3 -m pytest` |
| [b-federation-security-lab-fastapi](b-federation-security-lab-fastapi.md) | 시작 위치의 구현을 완성해 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다, TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다, recovery code 재생성 및 소진 규칙이 있어야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && PYTHONPATH=. python3 -m pytest` |
| [c-authorization-lab-fastapi](c-authorization-lab-fastapi.md) | 시작 위치의 구현을 완성해 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다, 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다, owner와 일반 member의 차이가 실제 리소스 접근에 반영되어야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && PYTHONPATH=. python3 -m pytest` |
| [d-data-api-lab-fastapi](d-data-api-lab-fastapi.md) | 시작 위치의 구현을 완성해 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다, 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다, 소프트 삭제가 목록 조회에 반영되어야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/D-data-api-lab/fastapi && PYTHONPATH=. python3 -m pytest` |
| [f-realtime-lab-fastapi](f-realtime-lab-fastapi.md) | 시작 위치의 구현을 완성해 WebSocket 연결이 인증된 사용자와 연결되어야 합니다, presence heartbeat가 TTL 기반으로 갱신되어야 합니다, 한 사용자에게 여러 활성 연결이 있어도 fan-out이 가능해야 합니다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/F-realtime-lab/fastapi && PYTHONPATH=. python3 -m pytest` |
| [h-service-boundary-lab-fastapi](h-service-boundary-lab-fastapi.md) | 시작 위치의 구현을 완성해 identity-service가 토큰을 발급한다, workspace-service가 그 토큰 claims만으로 workspace를 생성한다, 두 서비스가 각자 자기 DB만 읽고, cross-DB 조회를 하지 않는다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/H-service-boundary-lab/fastapi/gateway test` |
| [i-event-integration-lab-fastapi](i-event-integration-lab-fastapi.md) | 시작 위치의 구현을 완성해 댓글 생성이 outbox에 기록된다, relay 후 notification-service가 stream을 consume한다, 같은 consume를 두 번 실행해도 알림이 중복 저장되지 않는다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/I-event-integration-lab/fastapi/gateway test` |
| [j-edge-gateway-lab-fastapi](j-edge-gateway-lab-fastapi.md) | 시작 위치의 구현을 완성해 gateway가 /api/v1/auth/*, /api/v1/platform/* 경로를 유지한다, 로그인 후 쿠키가 gateway에서만 설정된다, 내부 호출에 X-Request-ID가 전달된다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/J-edge-gateway-lab/fastapi/gateway test` |
| [k-distributed-ops-lab-fastapi](k-distributed-ops-lab-fastapi.md) | 시작 위치의 구현을 완성해 gateway와 내부 서비스가 각각 /health/live, /health/ready, /ops/metrics를 제공한다, request id가 로그 문맥과 응답 헤더에 남는다, AWS target shape 문서가 실제 배포 완료처럼 쓰이지 않는다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
