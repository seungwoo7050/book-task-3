# Scheduling Simulator

## 이 프로젝트가 가르치는 것

`scheduling-simulator`는 단일 CPU 위에서 scheduling policy가 waiting time, response time, turnaround time을 어떻게 바꾸는지 숫자와 replay로 보여 주는 작은 실험이다.

## 누구를 위한 문서인가

- FCFS, SJF, RR, MLFQ를 한 번에 비교해 보고 싶은 학습자
- 운영체제 스케줄링을 코드와 fixture로 다시 설명하고 싶은 사람
- policy 차이를 표와 timeline으로 검증 가능한 형태로 남기고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`python/README.md`](python/README.md)
3. [`docs/README.md`](docs/README.md)
4. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
scheduling-simulator/
  README.md
  problem/
  python/
  docs/
  notion/
```

## 검증 방법

```bash
cd problem
make test
make run-demo
```

직접 실행은 `python -m os_scheduling --fixture <path> --policy <fcfs|sjf|rr|mlfq|all> --replay`를 사용한다.

검증에서 보는 핵심 신호:

- `convoy.json`에서 SJF 평균 waiting time이 FCFS보다 낮다.
- `convoy.json`에서 RR 평균 response time이 FCFS보다 낮다.
- replay 출력이 policy별로 deterministic하게 유지된다.

## 스포일러 경계

- 이 프로젝트는 외부 course artifact 없이 self-authored fixture와 구현만 사용한다.
- README는 policy 차이와 검증 흐름에 집중하고, 긴 설명은 `docs/`와 `notion/`으로 분리한다.

## 포트폴리오로 확장하는 힌트

- 같은 fixture를 CSV export로 저장해 plotting을 붙이면 시각화 프로젝트로 키울 수 있다.
- context switch cost나 I/O burst를 추가하면 더 현실적인 scheduler toy model로 확장할 수 있다.

## 현재 한계

- 실제 CPU scheduler처럼 sleep/wakeup이나 I/O burst를 다루지 않는다.
- MLFQ 파라미터는 교육용 deterministic 비교를 위한 고정값이다.
