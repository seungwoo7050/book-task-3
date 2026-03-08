# Strassen Recurrence

## CLRS Connection

CLRS Ch 4 replaces 8 sub-matrix multiplications with 7 multiplications plus additional additions.

## Study Notes

- 입력 크기가 2의 거듭제곱이 아닐 수 있으므로 padding이 필요하다.
- 작은 하위 문제에서는 고전적인 cubic multiplication으로 내려가는 것이 상수항 면에서 낫다.
- 출력 단계에서는 padding 영역을 다시 잘라내야 한다.
