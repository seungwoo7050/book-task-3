# Core Concepts

## 핵심 개념

- worker pool은 제한된 수의 goroutine으로 작업을 소비하는 패턴이다.
- pipeline은 단계별 channel 연결로 데이터 흐름을 분리한다.
- `context.Context`는 중단 신호를 한 방향으로 전파하는 공통 장치다.
- goroutine을 시작했다면 종료 경로와 channel close 책임도 같이 설계해야 한다.

## Trade-offs

- worker 수를 늘리면 처리량이 오를 수 있지만 contention과 context switch 비용도 오른다.
- pipeline은 읽기 쉽지만 stage가 많아질수록 디버깅이 어려워질 수 있다.

## 실패하기 쉬운 지점

- cancellation 후 channel drain이나 close 순서를 잘못 두면 goroutine leak가 생긴다.
- benchmark 숫자만 보고 실서비스 concurrency 정책으로 바로 옮기면 과적합될 수 있다.

