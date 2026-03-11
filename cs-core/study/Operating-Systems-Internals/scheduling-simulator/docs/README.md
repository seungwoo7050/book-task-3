# Scheduling Simulator 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 scheduler policy 이름을 외우는 데서 멈추지 않고, 어떤 지표를 봐야 policy 차이가 드러나는지 설명한다. 코드만 읽으면 잘 안 보이는 “왜 이 fixture에서 이 policy가 유리한가”를 문서로 정리하는 역할을 맡는다.

## 누구를 위한 문서인가

- scheduling chapter를 읽었지만 waiting/response/turnaround가 자꾸 섞이는 학습자
- RR와 MLFQ를 fairness 관점으로 설명하고 싶은 사람
- fixture와 replay를 어떻게 읽어야 하는지 먼저 알고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/scheduler-metrics.md`](concepts/scheduler-metrics.md)
2. [`concepts/policy-tradeoffs.md`](concepts/policy-tradeoffs.md)
3. [`concepts/mlfq-heuristics.md`](concepts/mlfq-heuristics.md)
4. [`references/verification.md`](references/verification.md)
5. [`references/README.md`](references/README.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    scheduler-metrics.md
    policy-tradeoffs.md
    mlfq-heuristics.md
  references/
    verification.md
    README.md
```

## 검증과 연결되는 파일

- replay와 summary shape는 [`../python/src/os_scheduling/core.py`](../python/src/os_scheduling/core.py)에서 만든다.
- policy 차이를 고정하는 golden test는 [`../python/tests/test_os_scheduling.py`](../python/tests/test_os_scheduling.py)에 있다.
- canonical 명령은 [`../problem/README.md`](../problem/README.md)에 있다.
- 구체 검증 신호는 [`references/verification.md`](references/verification.md)에 적어 둔다.

## 포트폴리오로 확장하는 힌트

- 같은 workload를 context switch overhead 유무로 나눠 비교하면 “toy model에서 production concern으로 확장되는 지점”을 설명하기 쉽다.
- policy별 평균값만이 아니라 worst-case waiting time을 같이 적으면 fairness 이야기가 더 선명해진다.
