# 0x16 Computational Geometry — 회고

## 배운 것

- 외적 하나로 방향, 넓이, 교차 판정 모두 가능
- Andrew's Monotone Chain이 Graham Scan보다 구현 단순 (atan2 불필요)
- 정수 좌표면 부동소수점 오차 없이 정확한 판정 가능

## 주의

실수 좌표에서는 epsilon 비교 필요. 이 프로젝트는 정수 좌표 전제.
