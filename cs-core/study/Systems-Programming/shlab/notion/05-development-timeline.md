# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 `shlab`을 다시 세울 때 공식 starter 없이도 셸의 상태 전이와 signal 규칙을 어떤 순서로 검증해야 하는지 보존하는 재현 문서입니다.
trace 이름보다 관찰 가능한 동작을 기준으로 다시 따라가는 데 목적이 있습니다.

## 권장 재현 순서

1. `problem/`에서 공개 boundary 상태를 먼저 확인한다.
2. `c/`에서 background job, stop/resume, reaping 흐름을 테스트로 통과시킨다.
3. `cpp/`에서도 같은 하네스를 다시 통과시킨다.
4. 이상이 있으면 signal masking과 `waitpid` 경로부터 다시 본다.

## 최소 명령

```bash
cd problem
make status

cd ../c
make clean && make test

cd ../cpp
make clean && make test
```

## 성공 신호

- `problem/` 상태 출력이 현재 공개 boundary와 일치한다.
- C track에서 `C shlab tests passed`가 나온다.
- background harness에서 `Running /bin/sleep 1 &`가 확인된다.
- stop/resume harness에서 `stopped by signal 18` 이후 종료 흐름이 맞는다.
- C++ track도 같은 직접 하네스를 통과한다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: 공개 boundary와 공식 starter 경계
- `../docs/concepts/signal-and-race-discipline.md`: masking 규칙
- `../docs/concepts/job-control-flow.md`: 상태 전이 모델
- `../docs/references/verification.md`: 현재 검증 명령과 기대 메시지
