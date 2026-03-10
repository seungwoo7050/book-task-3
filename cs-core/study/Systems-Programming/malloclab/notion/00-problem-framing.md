# 00. 문제 정의

## 문제를 어떻게 이해했는가

`malloclab`은 allocator 함수를 네 개 만드는 프로젝트가 아니라,
"힙 위에서 어떤 규칙이 항상 유지돼야 하는가"를 설계하는 프로젝트라고 봤다.

그래서 구현보다 먼저 다음을 정해야 했다.

- block layout
- alignment 규칙
- free list 불변식
- `realloc` 처리 순서

## 저장소 기준 성공 조건

- trace driver가 정렬, overlap, payload 보존을 확인한다
- C/C++ 구현이 같은 계약을 지킨다
- `realloc`의 in-place growth 여부까지 설명 가능하다
- 공개 문서가 allocator 불변식을 코드 밖에서도 설명한다

## 선수 지식

- header/footer 기반 block layout
- explicit free list
- `mem_sbrk()` 기반 heap 확장
- split/coalesce 기본 규칙
