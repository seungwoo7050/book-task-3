# Approach Log

## 세 갈래 길에서의 선택

프로젝트를 시작할 때, 설계 방향이 세 가지 있었다.

**첫 번째 선택지: 로컬 auth만 먼저 만든다.** 범위가 작고 디버깅이 쉽다. 하지만 OAuth까지 다루지 못하니 "인증 시스템"이라 부르기엔 절반짜리가 된다.

**두 번째 선택지: OAuth까지 한 번에 넣는다.** 기능이 풍부해 보이지만, 인증의 기본 보안 경계—비밀번호 해시, 이메일 검증, 토큰 rotation—가 provider 통합 과정에 묻혀버릴 위험이 있다.

**세 번째 선택지: header 기반 토큰만 쓰고 cookie를 아예 빼버린다.** 구현은 간단해지지만, cookie + CSRF라는 실무에서 반드시 마주치는 경계를 경험할 수 없다.

결국 첫 번째 방식을 골랐다. 핵심 이유는 이것이었다: **로컬 credential lifecycle에서 발생하는 모든 보안 결정을, 다른 주제와 섞이지 않는 상태로 경험하고 싶었다.** OAuth는 다음 랩에서 얼마든지 추가할 수 있지만, 기본기가 흔들리면 그 위에 뭘 올려도 불안하다.

## 구체적인 설계 결정들

방향이 정해진 뒤, 몇 가지 구체적인 설계 결정이 뒤따랐다.

**패키지 구조:** auth 중심의 단일 FastAPI workspace를 유지했다. `app/domain/services/auth.py`에 인증 비즈니스 로직을 모으고, `app/api/v1/routes/auth.py`에 HTTP 엔드포인트를, `app/repositories/`에 데이터 접근을 분리했다.

**데이터 저장소 분리:** 테스트는 SQLite로, Docker Compose 환경은 PostgreSQL로 분리했다. 테스트가 매번 PostgreSQL을 띄워야 했다면 반복 속도가 너무 느려졌을 것이다. 대신 SQLite와 PostgreSQL 사이의 미묘한 동작 차이(예: timezone 처리)가 남는다는 점은 인지하고 넘어갔다.

**보안 경계 설계:** short-lived access token (15분)과 rotating refresh token (14일)을 분리했다. 로그인 시 두 토큰 모두 HttpOnly cookie로 발행하고, CSRF token은 JavaScript에서 읽을 수 있는 별도 cookie로 내보냈다. 상태 변경 요청(`POST /token/refresh`, `POST /logout`)에는 CSRF 검증을 필수로 걸었다.

**메일 통합:** 실 SMTP가 아닌 Mailpit 중심의 로컬 개발 경험으로 방향을 잡았다. 테스트 환경에서는 `app.state.mailbox`라는 in-memory 리스트에 메일을 쌓아두어, 테스트 코드가 직접 토큰을 꺼내서 검증할 수 있게 했다.

## 왜 다른 길은 버렸는가

OAuth를 같은 랩에 넣는 방식은 명확하게 폐기했다. 인증 기본기보다 provider 통합이 더 크게 보이면, 이 랩의 존재 이유가 사라진다. "Argon2로 비밀번호를 해시해야 하는 이유"보다 "Google client_id를 어디에 넣어야 하는가"가 더 큰 문제가 되어버린다.

PostgreSQL 하나로 테스트를 돌리는 방식도 버렸다. 학습 저장소에서는 코드 한 줄 고치고 테스트를 다시 돌리는 반복이 빨라야 한다. DB 컨테이너를 매번 띄우는 비용을 감수할 이유가 없었다.

