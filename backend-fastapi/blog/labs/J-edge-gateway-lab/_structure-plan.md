# J-edge-gateway-lab Structure Plan

## 한 줄 약속
- public API shape는 edge에 남기고, 내부 서비스에는 bearer와 request id만 넘기기

## 독자 질문
- 서비스가 나뉘어도 브라우저는 하나의 API만 보게 하려면, cookie와 CSRF를 어디에 두고 내부 계약을 어떻게 단순화해야 하는가.
- 왜 public API를 gateway가 유지해야 하는가 왜 쿠키와 CSRF를 내부 서비스에 넘기지 않는가 request id는 어떤 경로로 전파되는가 upstream 오류는 어디서 어떤 HTTP 상태로 번역해야 하는가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 서비스 분리 뒤에도 public API shape를 유지해야 한다는 질문 세우기
2. gateway에 cookie와 bearer 번역 책임을 모으기
3. system test로 public path와 internal fan-out을 고정하기
4. 2026-03-10 재검증으로 gateway surface를 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/J-edge-gateway-lab/fastapi/gateway/app/api/v1/routes/platform.py::_auth_headers` — edge가 cookie를 bearer header로 번역해서 내부 서비스에 넘기는 최소 단서를 제공한다.
- 보조 앵커: `labs/J-edge-gateway-lab/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery` — public `/api/v1` 경로만 호출하면서 invite, comment, websocket 알림까지 이어지는 흐름을 보여 준다.
- 문서 앵커: `labs/J-edge-gateway-lab/problem/README.md`, `labs/J-edge-gateway-lab/docs/README.md`
- CLI 앵커:
- `make test (service unit tests)`
- `python -m pytest tests/test_system.py -q`
- `python -m tests.smoke`
- `docker compose up --build`

## 글에서 강조할 개념
- edge와 internal service의 책임 차이 gateway fan-out과 upstream 오류 표면화 방식 브라우저 상태와 서비스 간 계약의 분리 J 랩이 왜 “새 기능 추가”보다 “경계 재설계”에 가까운지
- edge gateway의 역할 cookie + CSRF를 edge로 모으는 이유 request id 전파 API gateway 제품 기능 전체를 복제하지 않습니다. rate limiting, circuit breaker, service discovery는 문서 수준으로만 남깁니다.

## 끝맺음
- 제외 범위: circuit breaker service discovery 고급 edge cache
- 검증 문장: 2026-03-10에 gateway/identity/workspace/notification unit test, system test, smoke가 모두 통과했다.
