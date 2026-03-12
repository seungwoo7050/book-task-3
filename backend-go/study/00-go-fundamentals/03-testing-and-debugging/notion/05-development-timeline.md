# 개발 타임라인 — 처음부터 끝까지

이 문서는 프로젝트 03을 처음부터 완성까지 만드는 전체 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 뼈대 만들기

### 1-1. 디렉터리 구조 생성

```bash
mkdir -p 00-go-fundamentals/03-testing-and-debugging/{solution/go/cmd/debugdemo,solution/go/analyzer,docs/concepts,docs/references,problem}
```

도메인 로직 패키지 이름을 `analyzer/`로 정했다. 로그를 분석하는 게 이 패키지의 역할이니까.

### 1-2. Go 모듈 초기화

```bash
cd 00-go-fundamentals/03-testing-and-debugging/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/03-testing-and-debugging
```

### 1-3. Workspace 등록

```bash
cd study
go work use 00-go-fundamentals/03-testing-and-debugging/go
```

---

## Phase 2: 파싱 로직 구현

### 2-1. Event struct와 ParseLine 함수 (`solution/go/analyzer/analyzer.go`)

`Event` struct: Category(string)와 DurationMS(int).

`ParseLine` 함수: `strings.Split`으로 쉼표 분리 → `strconv.Atoi`로 숫자 변환. 세 가지 에러 케이스(쉼표 없음, 숫자 아님, 빈 카테고리)를 각각 처리했다. 에러 래핑에 `fmt.Errorf("...: %w", err)`를 사용해서 원본 에러 체인을 유지했다.

### 2-2. Summarize 함수

라인 슬라이스를 받아서 category별 Summary(Count, TotalMS, AverageMS)를 map으로 반환. 평균을 매 이벤트마다 갱신하는 방식을 택했다. 정밀도보다 단순함을 우선한 결정이었다.

---

## Phase 3: Recorder 구현 (동시성)

### 3-1. 첫 번째 버전 — mutex 없이

처음에는 `sync.Mutex` 없이 슬라이스에 직접 append하는 `Recorder`를 만들었다.

### 3-2. race detector로 문제 발견

```bash
go test -race ./...
```

DATA RACE 경고가 나왔다. `Add`에서 슬라이스에 쓰는 동안 다른 goroutine도 쓰려고 해서 발생한 것이다.

### 3-3. sync.Mutex 추가

`Add`와 `Snapshot`에 모두 `r.mu.Lock()`/`defer r.mu.Unlock()`을 추가했다.

### 3-4. Snapshot의 복사 문제

`Snapshot`에서 `r.events`를 그대로 반환하면 lock 밖에서 race가 발생한다는 것을 race detector가 잡아줬다. `copy`로 독립 슬라이스를 만들어 반환하는 것으로 수정.

---

## Phase 4: 테스트 작성

### 4-1. TestParseLine — table-driven test + subtest

세 케이스(valid, missing comma, empty category)를 struct 슬라이스로 정의. `t.Run`으로 각 케이스에 이름을 붙여 subtest로 실행.

루프 변수 캡처 (`tc := tc`)를 넣어 `t.Parallel()`과 안전하게 사용.

### 4-2. TestSummarize

세 줄의 로그를 넣고 search의 평균이 150인지, checkout의 카운트가 1인지 확인.

### 4-3. TestRecorderSnapshot — 동시성 테스트

20개의 goroutine에서 동시에 `Add`를 호출하고, `sync.WaitGroup`으로 전부 끝나길 기다린 뒤 Snapshot의 길이를 확인. `-race` 플래그와 함께 실행해서 race가 없는지 검증.

### 4-4. BenchmarkSummarize

1000줄의 로그 데이터를 생성한 뒤 `b.ResetTimer()` 호출. `b.N` 루프에서 Summarize를 반복 실행.

---

## Phase 5: CLI 바이너리 작성

### 5-1. main.go 작성 (`solution/go/cmd/debugdemo/main.go`)

세 줄의 샘플 로그를 Summarize에 넣고 결과를 출력.

### 5-2. 실행

```bash
cd solution/go
go run ./cmd/debugdemo
# search count=2 avg_ms=100
# checkout count=1 avg_ms=150
```

---

## Phase 6: 전체 검증

### 6-1. 테스트 + 벤치마크

```bash
cd solution/go
go test ./... -bench=.
# ok   .../analyzer  0.XXXs
# BenchmarkSummarize-8  XXXXX  XXXXX ns/op
```

### 6-2. race detector

```bash
go test -race ./...
# ok   .../analyzer (race 경고 없음)
```

### 6-3. Makefile 통합

```bash
cd study
make test-new
make check-docs
```

### 6-4. 상태 확정

`verified` 상태로 변경.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.22+ | 컴파일, 실행, 테스트, 벤치마크, race detector |
| `go test -race` | 동시성 문제 자동 탐지 |
| `go test -bench=.` | 벤치마크 실행 |
| `sync.Mutex` | goroutine 간 상호 배제 |
| `sync.WaitGroup` | goroutine 완료 대기 (테스트용) |
| `make` | 전체 검증 |

외부 패키지 없음. 순수 표준 라이브러리 프로젝트.
