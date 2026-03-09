# 0x12 Red-Black Tree — 접근 과정

## RB-Tree 성질

1. 모든 노드는 RED 또는 BLACK
2. 루트는 BLACK
3. NIL(센티넬)은 BLACK
4. RED 노드의 자식은 모두 BLACK (연속 RED 불가)
5. 모든 경로의 black-height 동일

## 삽입 전략

새 노드를 RED로 삽입 후 `insert_fixup` 호출:
- **Case 1**: 삼촌이 RED → 부모·삼촌 BLACK, 조부모 RED, 조부모로 올라감
- **Case 2**: 삼촌 BLACK, 꺾인 형태 → 회전으로 Case 3 변환
- **Case 3**: 삼촌 BLACK, 직선 형태 → 부모 BLACK, 조부모 RED, 회전

## 회전

```python
def left_rotate(self, x):
    y = x.right
    x.right = y.left
    ...
```

포인터 5개 갱신. 대칭적 right_rotate도 동일 패턴.

## 중복 키 처리

이미 존재하면 삽입 스킵 — 집합 의미론.
