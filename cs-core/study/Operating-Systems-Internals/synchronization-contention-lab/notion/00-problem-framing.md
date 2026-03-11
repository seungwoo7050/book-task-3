# 00 Problem Framing

## 문제를 어떻게 이해했는가

이 프로젝트는 synchronization primitive API를 외우는 데서 멈추지 않고, “어떤 invariant를 지키기 위해 어떤 도구를 쓰는가”를 비교하는 실험이라고 이해했다. 그래서 모든 primitive를 같은 문제에 억지로 적용하지 않고, 각자 가장 잘 드러나는 시나리오를 골랐다.

## 저장소 기준 성공 조건

- counter final count가 expected count와 일치한다.
- gate max concurrency가 permit limit를 넘지 않는다.
- buffer produced와 consumed가 같고 underflow/overflow가 없다.
- shell test가 elapsed time이 아니라 invariant 위주로 판정한다.

## 고정 범위

- counter / gate / buffer 세 시나리오
- mutex / semaphore / condvar
- elapsed time, wait count, invariant metric 출력

## 제외 범위

- lock-free primitive
- rwlock
- sanitizer integration
- priority inversion 실험
