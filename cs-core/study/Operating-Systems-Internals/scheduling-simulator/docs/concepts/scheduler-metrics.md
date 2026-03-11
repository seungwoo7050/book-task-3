# Scheduler Metrics

## 왜 세 지표를 따로 보는가

스케줄러를 비교할 때 가장 자주 생기는 혼동은 “빨리 끝나는 것”과 “빨리 반응하는 것”을 같은 말로 취급하는 것이다. 실제로는 다음 세 지표가 서로 다른 질문을 던진다.

- waiting time: ready queue에서 CPU를 기다린 총 시간
- response time: arrival 후 처음 CPU를 잡기까지의 시간
- turnaround time: arrival 후 종료까지 걸린 전체 시간

## 이 프로젝트에서의 해석

- single burst 모델이라 `turnaround = waiting + burst`가 바로 성립한다.
- SJF는 평균 waiting time을 줄이는 쪽에 강하다.
- RR와 MLFQ는 response time을 낮추는 쪽에 강하다.
- 어떤 policy가 “좋다”는 말은 어느 지표를 우선하는지 먼저 말해야 의미가 생긴다.

## replay를 읽을 때 보는 포인트

1. 긴 job이 앞에서 CPU를 독점하는가
2. 짧은 job이 첫 응답을 언제 받는가
3. 마지막 completion 시점이 얼마나 뒤로 밀리는가
