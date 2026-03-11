# 00 Problem Framing

## 문제를 어떻게 이해했는가

이 프로젝트는 “scheduler를 구현한다”보다 “정책 차이를 결과 표와 replay로 설명 가능한 상태로 만든다”에 더 가깝다. 그래서 기능 수를 늘리는 대신, fixture와 출력 형식을 고정해 정책 비교가 흔들리지 않게 만드는 쪽을 우선했다.

## 저장소 기준 성공 조건

- FCFS, SJF, RR, MLFQ가 같은 workload를 deterministic하게 재현한다.
- policy별 평균 waiting / response / turnaround가 표로 비교된다.
- convoy와 interactive mix fixture가 각각 다른 tradeoff를 드러낸다.
- 테스트가 golden timeline과 policy 비교 assertion을 함께 가진다.

## 고정 범위

- single CPU
- integer tick
- single burst
- FCFS / non-preemptive SJF / RR / MLFQ

## 제외 범위

- I/O burst와 blocking
- context switch overhead
- multi-core
- priority inversion이나 starvation proof
