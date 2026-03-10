# Problem Framing

## 이 랩을 시작하게 된 배경

백엔드 인증을 공부할 때 가장 흔한 출발점은 "회원가입 API를 만들고, 로그인 API를 만들면 끝"이라는 식의 튜토리얼이다. 하지만 실제로 인증 시스템을 운영하다 보면, 비밀번호를 어떻게 저장하느냐, 세션을 어떻게 유지하느냐, 이메일 소유를 어떻게 증명하느냐, 비밀번호 분실 시 어떻게 복구하느냐 같은 문제가 줄줄이 따라온다. 이 문제들을 한꺼번에 풀려면 OAuth나 2FA 같은 외부 의존이 섞여서 핵심이 흐려지기 쉽다.

그래서 `A-auth-lab`은 **외부 identity provider 없이, 로컬 계정 흐름만으로 인증의 보안 경계를 전부 드러내는 것**을 목표로 잡았다. 회원가입부터 로그인, 이메일 검증, 비밀번호 재설정, rotating refresh token, secure cookie, CSRF 방어까지—이 모든 것이 하나의 credential lifecycle이라는 사실을 보여주는 게 핵심이다.

## 무엇을 만들어야 하는가

처음에 요구사항을 정리할 때, 크게 두 가지를 결정해야 했다.

**첫 번째는 프레임워크와 데이터 스택이다.** Python 3.12 이상, FastAPI를 기본 프레임워크로 쓰기로 했다. 데이터 저장소는 테스트에서 속도를 위해 SQLite를 쓰되, Docker Compose 환경에서는 PostgreSQL 16, Redis 7, 그리고 로컬 메일 검증용 Mailpit을 올리기로 했다.

**두 번째는 보안 경계의 범위다.** 비밀번호는 반드시 Argon2로 해시해야 하고, refresh token은 rotation을 지원해야 하며, cookie 기반 상태 변경 엔드포인트에는 CSRF 검증이 따라와야 한다. 반면 Google OAuth나 2FA는 다음 랩(`B-federation-security-lab`)으로 명시적으로 넘기기로 했다.

한 가지 고민이 더 있었다. 이메일 흐름을 실제 SMTP 서버로 보내야 할까, 아니면 Mailpit 같은 로컬 가짜 메일 서버를 쓸까. 결론은 후자였다. 학습 저장소에서는 "실제 메일이 날아가는가"보다 "이메일 검증 토큰이 제대로 발행되고 소비되는가"가 더 중요한 검증 포인트이기 때문이다.

## 성공 기준

이 랩이 끝났을 때 아래 조건이 모두 충족되어야 했다:

- **signup → login → email verification → password reset → refresh rotation** 전체 흐름이 동작할 것
- `make lint`, `make test`, `make smoke`, `docker compose up --build` 네 가지 명령이 현재 상태를 증명할 것
- CSRF mismatch, 만료된 reset token, 미인증 이메일 로그인 같은 **실패 경계가 테스트로 명확히 잡혀 있을 것**
- OAuth나 2FA가 이 랩에 들어있지 않다는 사실이 문서에 분명히 적혀 있을 것

## 남아 있던 불확실성

가장 큰 불확실성은 "Mailpit만으로 이메일 검증 경험을 충분히 보여줄 수 있는가"였다. 실제 Gmail이나 SMTP 서비스와의 연동 없이도 학습 목적은 달성할 수 있다고 판단했지만, 실 운영 환경에서의 전송 실패나 스팸 필터 같은 edge case는 이 랩의 범위를 넘어선다. 이 부분은 후속 랩이나 별도 실험으로 남겨두었다.

