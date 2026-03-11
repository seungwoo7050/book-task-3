# 01 Approach Log

## 설계 선택

- counter, gate, buffer를 같은 CLI 인터페이스로 노출해 demo와 테스트를 단순화했다.
- metric struct를 공통으로 두어 shell test가 시나리오별 field만 골라 읽도록 만들었다.
- correctness 판정은 각 시나리오 함수 안에서 `ok` 필드로 먼저 계산하고, CLI는 그 결과를 그대로 출력하게 했다.
- macOS 호환성을 위해 semaphore는 named POSIX semaphore로 구현했다.

## 시나리오를 나눈 이유

- counter는 lost update를 가장 단순하게 드러낸다.
- gate는 semaphore permit ceiling을 직접 보여 준다.
- buffer는 condvar와 `while` loop discipline을 설명하기에 가장 적합하다.
