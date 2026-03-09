# 문제 정의 — 왜 동시성 패턴인가

## Go의 동시성은 문법만으로는 부족하다

Go를 고른 이유 중 하나가 goroutine과 channel이다. 01에서 Go 문법을 배웠고, 03에서 `sync.Mutex`와 race detector를 만졌다. 하지만 "goroutine을 시작할 수 있다"는 것과 "goroutine을 안전하게 관리할 수 있다"는 전혀 다른 능력이다.

서버는 동시에 수백, 수천 개의 요청을 처리한다. 06-09에서 만든 HTTP 핸들러도 내부적으로 goroutine 위에서 돌아간다. 하지만 직접 goroutine을 생성하고, 채널로 통신하고, 종료를 보장하는 코드는 아직 작성하지 않았다.

## 핵심 과제

두 가지 패턴을 구현한다:

### Part 1: Worker Pool
- N개의 worker goroutine이 공유 채널에서 Job을 꺼내 처리
- 결과를 results 채널로 전달
- `Stop()`으로 graceful shutdown, context cancellation으로 즉시 종료
- goroutine 누수 없음

### Part 2: Pipeline
- Generator → Filter → Sink 3단계 파이프라인
- 각 단계가 별도 goroutine에서 실행
- 채널로 연결, context cancellation 지원
- FanOut으로 병렬 처리 확장

## 왜 이 시점인가

09까지 HTTP + SQL + 캐시를 다뤘다. 10에서 동시성의 기초 패턴을 익혀야 11(rate-limiter)에서 토큰 버킷을 goroutine으로 관리하고, 12(gRPC)에서 스트리밍을 다루고, 13(distributed-log)에서 복제 파이프라인을 구현할 수 있다.

## 외부 의존성 없음

이 프로젝트는 Go 표준 라이브러리만 사용한다. `context`, `sync`, `channel` — 이 세 가지가 Go 동시성의 전부다.
