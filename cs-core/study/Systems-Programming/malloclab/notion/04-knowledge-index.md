# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- block header/footer invariant: allocator가 무너질 때 가장 먼저 확인해야 하는 계약이다.
- explicit free list insert/remove 규칙: free list 조작이 흔들리면 이후 모든 버그가 연쇄적으로 생긴다.
- split과 coalesce 조건: 지나친 분할과 늦은 병합 모두 성능과 정합성을 동시에 해칠 수 있다.
- in-place `realloc` growth: 복사를 줄이는 핵심이지만, payload preservation 검증이 따라와야 안전하다.
- trace-driven payload preservation: allocator는 단순 crash-free보다 기존 payload를 보존하는지가 더 중요하다.

## 재현 중 막히면 먼저 확인할 것

- 불변식 문서: `../docs/concepts/allocator-invariants.md`
- `realloc` 전략: `../docs/concepts/realloc-and-coalescing.md`
- 현재 검증 순서와 요약 수치: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- 시스템 구현에서 불변식을 먼저 쓰고 코드를 맞추는 습관은 이 프로젝트가 가장 강하게 가르친다.
- 이후 어떤 저수준 자료구조를 다루더라도 "계약 -> 조작 규칙 -> 검증" 순서가 다시 필요해진다.
