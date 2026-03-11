# Scheduling Simulator

`scheduling-simulator`는 단일 CPU 위에서 scheduling policy가 waiting time, response time, turnaround time을 어떻게 바꾸는지 replay와 지표로 보여 주는 실험이다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| FCFS, SJF, RR, MLFQ가 같은 workload에서 어떤 지표 차이를 만드는지 비교한다. | 단일 CPU, deterministic fixture, 고정된 MLFQ 파라미터를 유지하고 I/O burst는 다루지 않는다. | 구현은 [`python/`](python/README.md)의 scheduler와 replay CLI, fixture, 지표 계산 로직으로 정리한다. | [`problem/README.md`](problem/README.md), [`python/README.md`](python/README.md) | fairness, response time, turnaround, replay 기반 검증 | `public verified` |

## 디렉터리 역할

- `problem/`: 문제 범위와 canonical `make` entrypoint
- `python/`: scheduler 구현과 CLI
- `docs/`: policy trade-off, metric 정의, MLFQ heuristic 정리
- `notion/`: fixture 설계와 재검증 기록

## 검증 빠른 시작

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

## 공개 경계

- 이 프로젝트는 외부 course artifact 없이 self-authored fixture와 구현만 사용한다.
- README는 policy 차이와 검증 흐름에 집중하고, 긴 설명은 `docs/`와 `notion/`으로 분리한다.

## 현재 한계

- 실제 CPU scheduler처럼 sleep/wakeup이나 I/O burst를 다루지 않는다.
- MLFQ 파라미터는 교육용 deterministic 비교를 위한 고정값이다.
