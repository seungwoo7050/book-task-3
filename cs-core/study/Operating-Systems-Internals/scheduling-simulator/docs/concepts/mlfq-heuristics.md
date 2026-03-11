# MLFQ Heuristics

## 왜 heuristic인가

MLFQ는 SJF처럼 미래 burst를 정확히 알지 못해도 interactive job을 앞세우고 싶을 때 쓰는 규칙 모음이다. 대신 규칙 수가 많아지고, 각 규칙을 어디에 두느냐에 따라 결과가 바뀐다.

## 이 프로젝트의 고정 규칙

- queue는 3단계다.
- quantum은 위에서부터 `1 / 2 / 4` tick이다.
- 새 job은 가장 높은 priority queue에서 시작한다.
- quantum을 모두 쓰고도 끝나지 않으면 한 단계 아래 queue로 내려간다.
- starvation 완화를 위해 10 tick마다 priority boost를 적용한다.

## 이 toy model에서 일부러 단순화한 것

- boost는 dispatch boundary에서만 적용한다.
- I/O burst와 sleep/wakeup은 다루지 않는다.
- dynamic priority decay나 per-process history는 넣지 않는다.

이 단순화 덕분에 테스트가 deterministic해지고, “왜 heuristic인지”를 설명하는 데 필요한 규칙만 남는다.
