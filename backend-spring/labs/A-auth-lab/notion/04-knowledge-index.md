# Knowledge Index — 이 랩에서 가져갈 개념들

## 재사용 가능한 핵심 개념

### Refresh Token Rotation

refresh token을 고정된 값이 아니라 **사용할 때마다 새 토큰으로 교체하는 패턴**이다. 이 랩의 `AuthDemoService.refresh()` 메서드가 정확히 이 동작을 보여준다 — 기존 refresh token을 `sessions`에서 제거하고, 새로운 refresh token을 발급해서 다시 저장한다.

이 패턴이 중요한 이유는 **토큰 탈취 감지**에 있다. 만약 공격자가 refresh token을 훔쳐서 사용하면, 정상 사용자가 같은 토큰으로 refresh를 시도할 때 "token not found" 에러가 발생한다. 이 시점에 서버는 해당 토큰 패밀리 전체를 무효화할 수 있다. 이 개념은 B-federation-security-lab에서 OAuth2 provider 연동 시 다시 등장하고, capstone에서 실제 Redis 기반 세션 관리로 확장된다.

### Mailpit-ready Workflow

실제 메일 provider(SendGrid, SES 등) 없이도 **로컬에서 verification/reset 메일 흐름을 관찰할 수 있는 학습 방식**이다. Docker Compose에 Mailpit 컨테이너를 포함시키면, SMTP 포트(1025)로 발송된 메일이 Mailpit 웹 UI(8025)에서 확인된다.

이 랩에서는 아직 실제 메일 발송 코드가 없지만, `spring-boot-starter-mail` 의존성과 `application.yml`의 mail 설정이 이미 준비되어 있어서, 코드 한 줄이면 Mailpit으로 메일을 보낼 수 있는 상태다. E-event-messaging-lab에서 이벤트 기반 메일 발송을 다룰 때 이 인프라가 그대로 재활용된다.

### Verified Scaffold

기능 범위는 제한적이지만 **lint, test, smoke, Compose boot가 모두 통과하는 상태**를 뜻한다. "코드가 있다"와 "검증된 코드가 있다"는 다른 말이다. 이 랩에서 정의한 scaffold의 조건은:

1. `make lint` — Spotless와 Checkstyle이 경고 없이 통과
2. `make test` — 모든 유닛/통합 테스트 통과
3. `make smoke` — 앱이 부팅되고 기본 엔드포인트가 응답
4. `docker compose up --build` — 전체 스택이 정상 기동

이 기준은 이후 모든 랩에서 동일하게 적용되는 품질 baseline이다.

## 용어 정리

### Contract-level Auth

security boundary를 **먼저 API shape로 설명하는 단계**를 뜻한다. 예를 들어 "POST /api/v1/auth/refresh는 X-CSRF-TOKEN 헤더와 refreshToken body를 받아서 새 세션을 반환한다"는 contract-level 설명이다. 실제 구현이 인메모리인지 DB 기반인지는 이 단계에서 중요하지 않다.

### Recovery Flow

계정 분실이나 비밀번호 재설정처럼 **예외 상황을 처리하는 인증 흐름**이다. 정상 흐름(register → login → use → logout)과는 별도의 경로를 가지며, 보통 이메일이나 SMS를 통한 본인 인증이 수반된다. 이 랩에서는 개념만 도입했고, 실제 구현은 후속 과제로 남겨두었다.

## 참고 자료

- **A-auth-lab docs README** (`docs/README.md`): 구현 범위와 다음 개선점을 맞추기 위해 작성했다. 현재는 modeled API와 lightweight persistence가 중심이라는 사실을 확인하고, 회고와 디버그 로그에서 scaffold 성격을 명시하는 데 반영했다.
- **Spring Security Reference** — `SecurityFilterChain` 기반 설정 방식과 CSRF 보호 메커니즘을 참고했다. 이 문서에서 "CSRF를 disable하면 어떤 보호가 사라지는지"를 확인한 뒤, 애플리케이션 레벨 CSRF 토큰 검증 방식을 선택하는 근거로 삼았다.

