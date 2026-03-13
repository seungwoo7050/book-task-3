# 09 Cache Migrations Observability Structure

## 이 글이 답할 질문

- cache-aside hit/miss와 invalidation을 같이 경험해야 한다.
- 운영성 기본기는 인프라 의존도를 낮춘 상태에서 먼저 익히도록 in-memory cache를 사용했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/09-cache-migrations-observability` 안에서 `10-runtime-and-migration-surface.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: 스키마 및 마이그레이션 정의 (app.go) -> 5단계: Seed 함수 -> 6단계: Service 구조체 정의
- 세션 본문: `solution/go/internal/app/app.go, solution/go/cmd/server/main.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/app/app.go`
- 코드 앵커 2: `solution/go/cmd/server/main.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.
- 마지막 단락: 다음 글에서는 `20-cache-invalidation-and-fallback.md`에서 이어지는 경계를 다룬다.
