# 07 Auth Session JWT Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - Claims와 Session을 나눠 auth 상태 모델을 먼저 세운다

- 목표: Claims와 Session을 나눠 auth 상태 모델을 먼저 세운다
- 변경 단위: `solution/go/internal/auth/server.go`의 `Claims`
- 핵심 가설: `Claims` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
- 반드시 넣을 코드 앵커: `Claims`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestSessionLoginAndProtectedResource`였다.
- 새로 배운 것 섹션 포인트: authentication은 “누구인가”를 확인하는 단계이고 authorization은 “무엇을 할 수 있는가”를 확인하는 단계다.
- 다음 섹션 연결 문장: loginSession, loginJWT와 protected route로 두 인증 경로를 연결한다
### 2. Phase 2 - loginSession, loginJWT와 protected route로 두 인증 경로를 연결한다

- 목표: loginSession, loginJWT와 protected route로 두 인증 경로를 연결한다
- 변경 단위: `solution/go/internal/auth/server.go`의 `loginJWT`
- 핵심 가설: `loginJWT`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `loginJWT`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestExpiredToken`였다.
- 새로 배운 것 섹션 포인트: JWT는 stateless라 편하지만 만료, revoke, 서명키 관리가 추가된다.
- 다음 섹션 연결 문장: server_test로 role, expiry, signature 검증을 잠근다
### 3. Phase 3 - server_test로 role, expiry, signature 검증을 잠근다

- 목표: server_test로 role, expiry, signature 검증을 잠근다
- 변경 단위: `solution/go/internal/auth/server_test.go`의 `TestJWTProtectedResource`
- 핵심 가설: `TestJWTProtectedResource` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `TestJWTProtectedResource`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestExpiredToken`였다.
- 새로 배운 것 섹션 포인트: 테스트에서 실제 bcrypt 해시를 쓰면 속도는 느려지지만 현실성은 높아진다. 작은 예제에서는 받아들일 만한 비용이다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/07-auth-session-jwt && cd solution/go && go test -v ./internal/auth)
```

```text
=== RUN   TestSessionLoginAndProtectedResource
=== PAUSE TestSessionLoginAndProtectedResource
=== RUN   TestJWTProtectedResource
=== PAUSE TestJWTProtectedResource
=== RUN   TestForbiddenRole
=== PAUSE TestForbiddenRole
=== RUN   TestExpiredToken
=== PAUSE TestExpiredToken
=== RUN   TestInvalidSignature
=== PAUSE TestInvalidSignature
=== CONT  TestSessionLoginAndProtectedResource
=== CONT  TestExpiredToken
=== CONT  TestForbiddenRole
=== CONT  TestJWTProtectedResource
=== CONT  TestInvalidSignature
--- PASS: TestForbiddenRole (0.17s)
--- PASS: TestExpiredToken (0.17s)
--- PASS: TestSessionLoginAndProtectedResource (0.23s)
--- PASS: TestJWTProtectedResource (0.24s)
--- PASS: TestInvalidSignature (0.29s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/07-auth-session-jwt/internal/auth	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/07-auth-session-jwt && cd solution/go && go test -run TestExpiredToken -v ./internal/auth)
```

```text
=== RUN   TestExpiredToken
=== PAUSE TestExpiredToken
=== CONT  TestExpiredToken
--- PASS: TestExpiredToken (0.15s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/07-auth-session-jwt/internal/auth	(cached)
```
