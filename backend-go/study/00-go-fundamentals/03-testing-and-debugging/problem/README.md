# 문제 정의

간단한 로그 라인을 파싱하고 category별 요약을 만들며, race-safe recorder를 구현한다.

## 성공 기준

- `"category,duration_ms"` 형식의 라인을 파싱한다.
- category별 평균 지연 시간을 계산한다.
- concurrent append가 가능한 recorder를 만든다.
- benchmark와 subtest를 포함한다.

## 제공 자료와 출처

- `study`에서 새로 설계한 canonical 문제다.
- 이 문서가 공개용 한국어 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/debugdemo`
- `cd solution/go && go test ./... -bench=.`

## 제외 범위

- pprof/trace 심화
- 외부 observability 도구
