# Actual Cost vs Amortized Cost

## CLRS Connection

CLRS Ch 17 shows that a single expensive operation does not imply a large average cost if previous operations bank enough credit.

## Study Notes

- `MULTIPOP`은 한 번에 많이 pop해도 각 원소는 push 이후 최대 한 번만 제거된다.
- binary counter increment는 carry chain이 길 수 있지만 각 비트의 총 flip 수는 제한된다.
- 이 프로젝트는 amortized claim을 실제 operation log의 누적 비용으로 확인한다.
