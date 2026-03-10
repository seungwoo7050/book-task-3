# Approach Log — 보안 강화를 하나의 랩으로 묶기까지

## 선택지를 놓고 고민한 지점들

이 랩을 설계할 때 가장 먼저 갈등한 건 **범위**였다. Google OAuth만 다루고 2FA를 빼면 단순하지만 session hardening이 약해진다. 2FA만 별도 랩으로 떼면 auth story가 너무 조각난다. fully real provider integration은 의미 있지만 scaffold 단계에서는 환경 의존성이 크다.

## 최종 선택: "higher assurance session"을 하나의 랩으로

결국 federation과 2FA를 하나의 workspace에 묶고, simulated provider contract를 유지하는 방향을 택했다. 초기 scaffold에서는 audit와 external identity linking의 방향성을 먼저 보여주는 데 집중했다. provider callback 이후에도 second factor와 throttling이 남는다는 점을 코드 구조로 드러내는 것이 핵심이었다.

## 의식적으로 폐기한 아이디어들

live Google Console 연동을 랩 필수 조건으로 두는 방안은 폐기했다 — 환경 설정에 시간이 소모된다.
audit logging을 빼는 방안도 폐기했다 — security lab에서 운영 관점이 빠지면 안 된다.

## 이 결정을 뒷받침하는 근거

- `FederationSecurityController.java` — Google authorize/callback, 2FA setup/verify, audit events 조회까지 하나의 컨트롤러에서 흐름 연결
- `FederationSecurityDemoService.java` — 모든 주요 동작에 audit event 기록
- `FederationSecurityApiTest.java` — 전체 흐름을 MockMvc로 증명
- `make test` — 위 테스트 통과 확인

