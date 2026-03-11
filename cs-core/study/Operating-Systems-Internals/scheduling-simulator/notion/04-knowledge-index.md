# 04 Knowledge Index

## 핵심 용어

- scheduler metrics: waiting / response / turnaround
- convoy effect: 긴 job이 뒤의 짧은 job을 전부 묶어 두는 현상
- round-robin fairness: 모두가 CPU를 조금씩 받게 만드는 단순 fairness 기준
- MLFQ boost: 낮은 queue에 오래 머문 job을 다시 올려 starvation을 완화하는 규칙

## 같이 보면 좋은 파일

- `../docs/concepts/scheduler-metrics.md`
- `../docs/concepts/policy-tradeoffs.md`
- `../docs/concepts/mlfq-heuristics.md`
- `../python/tests/test_os_scheduling.py`
