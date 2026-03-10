# `realloc`과 coalescing을 어떻게 이해할까

## 왜 이 둘을 같이 봐야 하는가

`malloclab`에서 allocator가 성숙해지는 지점은 `realloc`을 넣을 때입니다.
단순 `malloc-copy-free`만 해도 동작은 하지만, 바로 앞뒤 free block을 어떻게 다루는지가 설계 차이를 만듭니다.

## immediate coalescing을 택한 이유

이 저장소는 free 직후 바로 coalescing하는 정책을 사용합니다.

장점:

- 큰 요청을 받을 때 다시 heap을 늘릴 가능성이 줄어든다
- heap 상태를 손으로 추적하기 쉽다
- `realloc`이 다음 free block으로 확장될 여지가 늘어난다

단점도 있지만, 학습용으로는 reasoning이 더 단순해지는 장점이 큽니다.

## allocation placement

first-fit explicit free list 위에서 다음 둘을 결정합니다.

- remainder가 충분히 크면 split
- 아니면 통째로 소비

핵심은 "쓸모없는 작은 조각을 만들지 않는 것"입니다.

## `realloc` 처리 순서

이 저장소는 보통 아래 순서로 `realloc`을 봅니다.

1. `ptr == NULL`이면 `malloc`
2. `size == 0`이면 `free`
3. 현재 block이 이미 충분히 크면 shrink 또는 그대로 사용
4. 다음 block이 free이고 합치면 충분하면 in-place growth
5. 아니면 allocate-copy-free

이 순서를 고정하면 구현과 디버깅 둘 다 쉬워집니다.

## 꼭 확인해야 할 실수

- `realloc` copy 길이를 새 크기로만 잡는 실수
- in-place growth 후 남은 부분 split 누락
- coalescing 후 free list 링크 정리 누락

`realloc`은 포인터 하나의 문제가 아니라 "기존 데이터가 얼마나 살아남는가"의 문제입니다.
