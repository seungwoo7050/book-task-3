# 04 Knowledge Index

## 핵심 용어

- mutex: shared state를 하나씩 직렬화하는 기본 primitive
- semaphore: permit count로 동시 진입을 제한하는 primitive
- condition variable: 조건 충족 전까지 sleep/wake를 조정하는 primitive
- bounded buffer: producer/consumer가 shared queue occupancy를 함께 관리하는 고전 예제

## 같이 보면 좋은 파일

- `../docs/concepts/mutex-semaphore-condvar.md`
- `../docs/concepts/correctness-before-timing.md`
- `../docs/concepts/scenario-invariants.md`
- `../c/tests/test_cases.sh`
