# 02. 디버그 기록

## 실제로 다시 확인한 포인트

### 1. URI에 포트가 없을 때 기본값 누락

`http://example.com/path` 형태에서 `port`를 빈 문자열로 두면 upstream 연결이 바로 실패한다.
기본값 `80` 처리 여부를 먼저 확인해야 했다.

### 2. required header 재작성 누락

클라이언트 header를 그대로 믿으면 과제 계약과 다르게 동작한다.
`Host`, `User-Agent`, `Connection`, `Proxy-Connection`은 proxy가 다시 써야 했다.

### 3. `SIGPIPE` 처리

upstream 또는 client가 먼저 끊으면 proxy 전체가 죽을 수 있다.
네트워크 과제에서는 이 한 줄 처리가 생각보다 중요했다.

### 4. cache lock을 쥔 채 I/O 하는 문제

cache hit 시 lock을 잡은 채 client write를 하면 동시성이 급격히 나빠진다.
lock 안에서는 복사만 하고, write는 밖에서 해야 했다.
