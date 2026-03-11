# Policy Tradeoffs

## FCFS

- 장점: 구현이 단순하고 replay가 가장 직관적이다.
- 약점: 긴 job 하나가 뒤의 짧은 job 전부를 막는 convoy effect가 쉽게 나타난다.

## SJF

- 장점: 평균 waiting time을 줄이는 예제가 많다.
- 약점: 실제 시스템에서는 미래 burst를 정확히 알 수 없으므로 이상적인 비교 기준에 가깝다.

## RR

- 장점: 각 job이 비교적 빨리 첫 응답을 받는다.
- 약점: quantum이 너무 작으면 context switch overhead가 커지는 방향으로 확장된다.

## MLFQ

- 장점: 짧고 interactive한 job을 우선해 response time을 낮추는 heuristic으로 읽기 좋다.
- 약점: boost 주기, queue 수, demotion 규칙 같은 파라미터에 민감하다.

이 프로젝트의 목적은 “어느 하나가 절대적으로 우월하다”를 증명하는 것이 아니라, 같은 fixture에서 어떤 지표가 어떻게 달라지는지 설명 가능한 상태를 만드는 것이다.
