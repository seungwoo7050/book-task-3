# 01 Go Syntax And Tooling Evidence Ledger

## 10 first-go-run-loop

- 시간 표지: Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 핵심 로직 구현 -> Phase 3: CLI 바이너리 작성 -> Phase 4: 테스트 작성 및 검증 -> Phase 5: 문서 작성 -> Phase 6: 최종 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/`, `problem/`, `docs/`, `study/`, `solution/go/lesson/lesson.go`, `solution/go/cmd/toolingdemo/main.go`
- 처음 가설: CLI보다 문자열 처리 핵심 로직을 먼저 분리해 문법 학습이 I/O 처리에 묻히지 않게 했다.
- 실제 조치: 디렉터리 구조 생성 이 프로젝트는 study 디렉터리 아래에 위치한다. Go 소스는 `solution/go/` 하위에, 과제 명세는 `problem/`에, 학습 문서는 `docs/`에 분리했다. lesson 패키지 작성 (`solution/go/lesson/lesson.go`) 가장 먼저 `Summary` struct를 정의했다. 함수의 반환값을 struct로 묶는 Go 관용구를 입문 단계부터 익히기 위한 선택이었다.

CLI:

```bash
mkdir -p 00-go-fundamentals/01-go-syntax-and-tooling/{solution/go/cmd/toolingdemo,solution/go/lesson,docs/concepts,docs/references,problem}

cd 00-go-fundamentals/01-go-syntax-and-tooling/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling
```

- 검증 신호:
- `main` 함수는 기본 입력 문자열을 가지고 있고, `os.Args`에 인자가 있으면 그걸 사용한다. `lesson.BuildSummary`를 호출하고 결과를 `fmt.Printf`로 출력한다.
- 출력: total=10 unique=8 top=go
- 출력: total=3 unique=2 top=hello
- ok   github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling/lesson
- --- PASS: TestBuildSummary (0.00s)
- 핵심 코드 앵커: `solution/go/lesson/lesson.go`
- 새로 배운 것: `strings.FieldsFunc`는 텍스트를 직접 루프 돌며 자르지 않아도 되는 표준 라이브러리 선택지다.
- 다음: stdin 입력과 flag 파싱은 현재 범위 밖이라 별도 검증하지 않았다.
