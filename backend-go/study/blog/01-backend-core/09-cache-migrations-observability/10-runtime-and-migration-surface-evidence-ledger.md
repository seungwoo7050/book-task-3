# 09 Cache Migrations Observability Evidence Ledger

## 10 runtime-and-migration-surface

- 시간 표지: 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: 스키마 및 마이그레이션 정의 (app.go) -> 5단계: Seed 함수 -> 6단계: Service 구조체 정의
- 당시 목표: cache-aside hit/miss와 invalidation을 같이 경험해야 한다.
- 변경 단위: `solution/go/internal/app/app.go`, `solution/go/cmd/server/main.go`
- 처음 가설: 운영성 기본기는 인프라 의존도를 낮춘 상태에서 먼저 익히도록 in-memory cache를 사용했다.
- 실제 조치: 08과 동일한 패턴이지만, 08의 `products`와 구분하기 위해 `items` 테이블을 사용. `mu`: 캐시 맵 동시 접근 보호 `metrics`: atomic 카운터로 lock-free 집계

CLI:

```bash
cd study/01-backend-core/09-cache-migrations-observability/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/09-cache-migrations-observability

go get modernc.org/sqlite
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/internal/app/app.go`
- 새로 배운 것: cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.
- 다음: 다음 글에서는 `20-cache-invalidation-and-fallback.md`에서 이어지는 경계를 다룬다.
