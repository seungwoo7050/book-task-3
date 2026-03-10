# allocator 불변식을 먼저 잡아야 하는 이유

## 이 프로젝트가 코드보다 규칙이 먼저인 이유

`malloclab`은 함수 수가 적지만, 내부 상태가 조금만 틀어져도 전체가 무너집니다.
그래서 구현 세부보다 먼저 "무엇이 항상 참이어야 하는가"를 세우는 편이 좋습니다.

## 블록 레이아웃 불변식

이 저장소의 allocator는 다음 구조를 가정합니다.

- 8바이트 header
- 8바이트 footer
- payload

free block은 payload 앞부분 16바이트를 free-list 링크로 씁니다.
그래서 최소 block 크기는 32바이트가 됩니다.

## 정렬 불변식

반환되는 payload pointer는 항상 16바이트 정렬이어야 합니다.
이 규칙은 다음 세 곳에서 동시에 지켜야 합니다.

- block size round-up
- prologue/epilogue 초기화
- split 후 새 block 배치

한 곳만 어긋나도 trace에서 바로 깨집니다.

## free list 불변식

- free list에 있는 block은 모두 free 상태여야 한다
- allocated block이 free list에 남아 있으면 안 된다
- 인접 free block이 coalescing 없이 따로 남아 있으면 안 된다
- remove/insert 시 양쪽 링크가 모두 맞아야 한다

이 불변식을 문장으로 말할 수 있어야 디버깅도 빨라집니다.

## driver가 실제로 확인하는 것

이 저장소의 trace driver는 단순히 crash 여부만 보지 않습니다.

- payload pointer 정렬
- live block 간 overlap 없음
- `realloc` 전 prefix 데이터 보존
- trace 종료 시 logical error 없음

그래서 "일단 돌아간다" 수준보다 한 단계 더 강한 검증이 가능합니다.
