# Replacement Policies

## FIFO

- 장점: 구현이 가장 단순하다.
- 약점: locality를 거의 반영하지 못해 Belady anomaly 같은 반직관적 결과가 나온다.

## LRU

- 장점: 최근 사용 이력을 활용해 temporal locality에 잘 맞는다.
- 약점: 완전한 LRU를 정확히 구현하는 비용은 크다.

## Clock

- 장점: reference bit 하나로 LRU를 값싸게 근사한다.
- 약점: hand 순서와 bit reset 타이밍을 이해하지 못하면 결과가 직관적이지 않을 수 있다.

## OPT

- 장점: “이 trace에서 가능한 최선”이라는 비교 기준선을 준다.
- 약점: 미래 접근을 아는 비현실적 가정이므로 실제 구현 정책은 아니다.
