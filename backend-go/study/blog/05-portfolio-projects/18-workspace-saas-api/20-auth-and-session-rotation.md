# 18 Workspace SaaS API — Auth And Session Rotation

`05-portfolio-projects/18-workspace-saas-api`는 JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다. 이 글에서는 Phase 4 — auth 패키지 (토큰 생성/검증) 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 4 — auth 패키지 (토큰 생성/검증)

## Day 1
### Session 1

- 당시 목표: owner/admin/member RBAC와 invitation, project/issue/comment 흐름을 제품형 도메인으로 묶었다.
- 변경 단위: `crypto/rand`, `internal/auth/tokens.go`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 진행: HMAC-SHA256 JWT: Header.Payload.Signature, base64url 인코딩 Claims: user_id, email, display_name, exp (15분) Refresh token: `crypto/rand` 32바이트 → hex 인코딩 (64자) 저장: SHA256(opaque_token) → DB의 token_hash 컬럼 ParseRefreshToken: hex decode → SHA256 해시 → DB 조회 테스트:

CLI:

```bash
go test ./internal/auth/ -v -count=1
```

검증 신호:

- - Refresh token: `crypto/rand` 32바이트 → hex 인코딩 (64자)
- - 저장: SHA256(opaque_token) → DB의 token_hash 컬럼
- - ParseRefreshToken: hex decode → SHA256 해시 → DB 조회

핵심 코드: `solution/go/internal/auth/tokens.go`

```go
var (
	// ErrInvalidToken은 토큰 형식이나 서명이 유효하지 않을 때 반환된다.
	ErrInvalidToken = errors.New("invalid token")
	// ErrExpiredToken은 토큰 만료 시 반환된다.
	ErrExpiredToken = errors.New("expired token")
)

// Claims는 액세스 토큰에 담기는 사용자 클레임이다.
type Claims struct {
	Sub   string `json:"sub"`
	Email string `json:"email"`
	Exp   int64  `json:"exp"`
}

// SignAccessToken은 HMAC으로 서명한 JWT 호환 액세스 토큰을 만든다.
func SignAccessToken(secret []byte, claims Claims) (string, error) {
	header := base64.RawURLEncoding.EncodeToString([]byte(`{"alg":"HS256","typ":"JWT"}`))
	payloadBytes, err := json.Marshal(claims)
```

왜 이 코드가 중요했는가:

이 코드는 인증 경계를 말이 아니라 서명 규칙과 상태 전이로 고정한다. access token과 refresh/session 흐름이 실제로 어떻게 분리되는지 보여 주는 기준점이다.

새로 배운 것:

- access token은 짧게, refresh token은 회전시키며 Redis에 필수 상태를 둔다.

보조 코드: `solution/go/internal/repository/store.go`

```go
var (
	ErrNotFound               = errors.New("not found")
	ErrEmailExists            = errors.New("email already exists")
	ErrOrganizationSlugExists = errors.New("organization slug already exists")
	ErrAlreadyMember          = errors.New("user is already a member")
	ErrPendingInvitation      = errors.New("pending invitation already exists")
	ErrProjectKeyExists       = errors.New("project key already exists")
	ErrVersionConflict        = errors.New("version conflict")
	ErrIdempotencyConflict    = errors.New("idempotency key conflict")
)

type Store struct {
	db *sql.DB
}

func Open(ctx context.Context, databaseURL string) (*Store, error) {
	db, err := sql.Open("pgx", databaseURL)
	if err != nil {
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

CLI:

```bash
cd 05-portfolio-projects/18-workspace-saas-api/go
go test ./...
make e2e
make smoke

cd ../../..
make test-portfolio-unit test-portfolio-repro
make test-all
```

검증 신호:

- `go test ./...` 통과
- `make e2e` 통과
- `make smoke` 통과
- [presentation-assets/demo-2026-03-07](presentation-assets/demo-2026-03-07)는
- `make test-portfolio-unit test-portfolio-repro` 통과

다음:

- 다음 글에서는 `30-repository-service-cache-boundaries.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/auth/tokens.go` 같은 결정적인 코드와 `cd 05-portfolio-projects/18-workspace-saas-api/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
