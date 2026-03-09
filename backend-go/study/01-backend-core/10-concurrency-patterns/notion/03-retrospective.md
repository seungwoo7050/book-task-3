# 회고 — 동시성 패턴을 직접 만들어본 뒤

## 무엇을 만들었나

Worker Pool과 Pipeline 두 가지 동시성 패턴. 각각 별도 패키지(`workerpool/`, `pipeline/`)로 분리하고, CLI 예제(`cmd/`)와 테스트를 함께 작성했다. 외부 의존성 없이 Go 표준 라이브러리만 사용.

## 잘된 점

**Worker Pool의 종료 경로가 명확하다.** Stop → close(jobs) → worker가 for-range 탈출 → wg.Done → wg.Wait 완료 → close(results). 이 체인이 한눈에 보인다.

**Pipeline의 조합성이 높다.** `Generate | Filter | Sink`를 자유롭게 연결할 수 있고, `FanOut`으로 병렬 처리도 가능하다. 각 함수가 `<-chan int`를 반환하는 시그니처 덕분에 Unix 파이프처럼 체이닝된다.

**context cancellation이 모든 곳에 일관적으로 적용됐다.** Worker, Generate, Filter, Sink, FanOut 전부 context를 받고, 취소 시 즉시 반환한다.

## 아쉬운 점

**타입이 고정되어 있다.** Pipeline은 `int` 전용이고, Worker Pool의 Payload는 `any`라 타입 안전성이 부족하다. Go 1.18 제네릭을 쓰면 `Pool[T]`, `Pipeline[T]`로 만들 수 있지만, 패턴 학습에 집중하려고 단순 타입을 선택했다.

**에러 처리가 Worker Pool에서만 있다.** Pipeline에서 Generator나 Filter가 에러를 만나면 어떻게 전파할까? `chan struct{ Value int; Err error }` 같은 구조를 쓰면 되지만, 복잡성 대비 이 프로젝트에서는 필요 없었다.

**FanOut 결과의 순서가 보장되지 않는다.** 여러 goroutine이 동시에 처리하므로 입력 순서와 출력 순서가 다르다. 순서가 중요하면 결과에 인덱스를 붙여야 한다.

## 이전 프로젝트와의 연결

- 03의 `sync.Mutex`와 `-race` 플래그가 여기서도 직접 관련된다
- 09의 `atomic.Int64` 카운터는 worker pool의 메트릭에 적용할 수 있는 패턴
- 06-09의 HTTP 서버 내부에서도 goroutine이 동작하지만, 직접 관리하지 않았음

## 다음 프로젝트로의 전달

11(rate-limiter)에서 토큰 버킷의 refill을 goroutine으로 관리한다. 10에서 배운 "goroutine 시작 → channel 통신 → context로 종료" 패턴이 직접 재활용된다.
