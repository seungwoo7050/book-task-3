# Python 구현 안내

## 구현 범위

- FCFS, non-preemptive SJF, RR, MLFQ policy 실행기
- JSON fixture parser와 deterministic state model
- policy별 replay formatter와 평균 metrics summary

## 어디서부터 읽으면 좋은가

1. `python/src/os_scheduling/core.py`: policy별 state transition이 실제로 구현된 파일이다.
2. `python/src/os_scheduling/cli.py`: fixture 입력, policy 선택, replay 출력 인터페이스를 본다.
3. `python/tests/test_os_scheduling.py`: golden timeline과 policy 비교 기준을 확인한다.

## 디렉터리 구조

```text
python/
  README.md
  src/os_scheduling/
    __main__.py
    cli.py
    core.py
  tests/
    test_os_scheduling.py
```

## 기준 명령

- 검증: `make -C ../problem test`
- demo: `make -C ../problem run-demo`
- 직접 실행: `PYTHONPATH=src python3 -m os_scheduling --fixture ../problem/data/convoy.json --policy all --replay`

## 구현에서 먼저 볼 포인트

- RR는 quantum 경계에서 새 arrival enqueue 순서가 바뀌면 replay가 흔들린다.
- MLFQ는 boost 시점이 tick 도중인지 dispatch 경계인지 명확해야 deterministic test가 가능하다.
- metrics는 timeline에서 다시 계산하지 않고 process state의 `start`, `completion`, `burst`를 기준으로 만든다.

## 현재 범위

- single CPU
- integer tick
- single burst per process
- context switch overhead 없음
