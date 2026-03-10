# Shell Lab 검증 기록

## 문제 경계 확인

```bash
cd problem
make status
```

2026-03-10 기준 기록:

- `problem/`은 계약 설명만 남긴 public boundary다
- 공식 starter shell, trace, Perl driver는 공개 트리에 없다
- 실제 검증은 C/C++ 구현과 shared direct harness에서 수행한다

## C 구현 검증

```bash
cd c
make clean && make test
```

검증 범위:

- FIFO 기반 direct shell launch
- background job 상태와 `jobs` 출력 확인
- 실제 shell PID에 `SIGINT` 전달 후 `terminated by signal` 확인
- stopped foreground job을 `fg`로 되살린 뒤 다시 interrupt

기록:

- `C shlab tests passed`
- background job harness에서 `Running /bin/sleep 1 &` 확인
- signal harness에서 `terminated by signal 2` 확인
- stop/resume harness에서 `stopped by signal 18` 이후 종료 확인

## C++ 구현 검증

```bash
cd cpp
make clean && make test
```

기록:

- C track과 같은 direct signal/stop-resume 검증 통과

## 현재 판단

이 프로젝트는 단순 compile 수준이 아니라,
job control과 signal forwarding의 실제 의미를 검증하는 수준까지 도달해 있습니다.
