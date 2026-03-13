# 07 Auth Session JWT Structure

## 이 글이 답할 질문

- cookie session과 bearer JWT를 둘 다 경험해야 한다.
- session과 JWT를 같은 프로젝트에 두어 저장 위치와 검증 흐름 차이를 직접 비교하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/07-auth-session-jwt` 안에서 `10-session-and-jwt-entrypoints.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: Server 구조체 정의 (internal/auth/server.go) -> 5단계: 사용자 초기화 (initUsers) -> 6단계: 라우트 등록 -> 7단계: 세션 로그인 구현 -> 8단계: JWT 로그인 구현
- 세션 본문: `require golang.org/x/crypto v0.48.0, METHOD /path, crypto/rand, Set-Cookie: session_token=...; HttpOnly; Path=/; SameSite=Strict` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/auth/server.go`
- 코드 앵커 2: `solution/go/cmd/server/main.go`
- 코드 설명 초점: 이 코드는 인증 경계를 말이 아니라 서명 규칙과 상태 전이로 고정한다. access token과 refresh/session 흐름이 실제로 어떻게 분리되는지 보여 주는 기준점이다.
- 개념 설명: authentication은 “누구인가”를 확인하는 단계이고 authorization은 “무엇을 할 수 있는가”를 확인하는 단계다.
- 마지막 단락: 다음 글에서는 `20-auth-boundary-and-test-closure.md`에서 이어지는 경계를 다룬다.
