# 0x16 Computational Geometry — 접근 과정

## Cross Product (방향 판정)

```python
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
```

- 양수: 반시계 방향 (CCW)
- 음수: 시계 방향 (CW)
- 0: 일직선 (collinear)

## Convex Hull: Andrew's Monotone Chain

1. 점들을 x좌표 기준 정렬
2. Lower hull: 왼쪽→오른쪽, CW가 아닌 점 제거
3. Upper hull: 오른쪽→왼쪽, 동일 로직
4. 합치기

$O(n \log n)$ — 정렬이 지배적.

## Segment Intersection

두 선분 $(a,b)$, $(c,d)$의 교차:
1. `cross(a,b,c)` × `cross(a,b,d)` ≤ 0 AND `cross(c,d,a)` × `cross(c,d,b)` ≤ 0
2. Collinear인 경우 `on_segment` 검사로 겹침 확인
