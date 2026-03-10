# 01. 접근 기록

## 실제로 택한 접근

이 프로젝트는 함수 구현 순서보다 상태 불변식 순서를 먼저 정했다.

1. block layout과 최소 block 크기 결정
2. explicit free list insert/remove 정리
3. placement와 split
4. free와 coalescing
5. 마지막에 `realloc`

## 왜 이렇게 했는가

- free list가 흔들리면 나머지 모든 경로가 불안정해진다
- `realloc`은 앞선 모든 규칙이 맞아야 제대로 구현된다
- trace driver를 강하게 해 두면 문서 설명도 쉬워진다

## 의도적으로 택한 설계

- explicit free list
- immediate coalescing
- next free block이 있으면 in-place `realloc` growth 시도
