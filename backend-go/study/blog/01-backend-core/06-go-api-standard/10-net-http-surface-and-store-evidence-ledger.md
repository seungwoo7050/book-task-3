# 06 Go API Standard Evidence Ledger

## 10 net-http-surface-and-store

- 시간 표지: Phase 1: 프로젝트 뼈대와 구조 결정 -> Phase 2: 데이터 레이어 구현
- 당시 목표: 표준 라이브러리만으로 RESTful JSON API를 설계해야 한다.
- 변경 단위: `cmd/api/`, `internal/data/models.go`, `internal/data/movies.go`
- 처음 가설: 외부 프레임워크를 빼고 표준 라이브러리만 사용해 HTTP 기초를 드러냈다.
- 실제 조치: 디렉터리 구조 생성 05번과 달리 `cmd/api/`에 여러 Go 파일을 두는 구조를 택했다. 같은 `main` 패키지에 속하는 파일들을 역할별로 분리한다. Movie struct 정의 (`internal/data/models.go`) `Movie` struct에 JSON 태그를 포함. `Version` 필드는 낙관적 잠금을 위한 것이지만 이 과제에서는 아직 사용하지 않는다. `Models` struct는 `MovieStore`를 감싸서 의존성 주입 포인트 역할.

CLI:

```bash
mkdir -p 01-backend-core/06-go-api-standard/{solution/go/cmd/api,solution/go/internal/data,docs/concepts,docs/references,problem}

cd 01-backend-core/06-go-api-standard/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/internal/data/movies.go`
- 새로 배운 것: `application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다.
- 다음: 다음 글에서는 `20-middleware-shutdown-and-proof.md`에서 이어지는 경계를 다룬다.
