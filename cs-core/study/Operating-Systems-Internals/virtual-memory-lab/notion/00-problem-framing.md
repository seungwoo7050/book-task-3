# 00 Problem Framing

## 문제를 어떻게 이해했는가

이 프로젝트는 virtual memory 전체를 구현하는 것이 아니라, trace를 따라가며 “왜 이 접근에서 fault가 났는가”를 설명 가능한 상태로 만드는 데 초점을 둔다. 그래서 page table, TLB, swap daemon보다 replacement policy와 locality를 먼저 고정했다.

## 저장소 기준 성공 조건

- FIFO, LRU, Clock, OPT가 같은 trace를 deterministic하게 재현한다.
- Belady anomaly가 FIFO에서 실제로 보인다.
- locality trace에서 LRU/OPT의 장점이 assertion으로 남는다.
- dirty trace가 dirty eviction count를 분명히 드러낸다.

## 고정 범위

- trace 기반 page replacement
- frame count parameter
- dirty bit와 dirty eviction count
- FIFO / LRU / Clock / OPT

## 제외 범위

- TLB
- page table walk
- swap daemon
- real disk latency model
