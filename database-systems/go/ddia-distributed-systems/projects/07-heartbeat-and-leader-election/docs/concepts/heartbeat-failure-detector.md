# Heartbeat Failure Detector

이 프로젝트의 failure detector는 아주 단순합니다. leader heartbeat를 일정 tick 동안 못 보면 follower가 “leader가 죽었을 수 있다”고 suspect합니다.

## 이 구현의 규칙

- leader는 고정된 주기마다 heartbeat를 전송합니다.
- follower는 heartbeat를 받으면 silence age를 0으로 되돌립니다.
- silence age가 `suspicionTTL` 이상이면 `Suspected=true`가 됩니다.
- silence age가 `electionTTL` 이상이면 election을 시작합니다.

## 왜 suspicion 단계가 따로 필요한가

heartbeat를 한 번 놓쳤다고 즉시 election으로 가면 상태 변화가 너무 갑작스럽게 보입니다. suspicion을 한 tick이라도 분리하면 “장애 신호가 먼저 보이고, 그 다음 authority 교체가 시작된다”는 흐름이 더 잘 드러납니다.

## 여기서 다루지 않는 것

- phi accrual failure detector
- network partition과 asymmetric loss
- lease timeout과 clock drift
