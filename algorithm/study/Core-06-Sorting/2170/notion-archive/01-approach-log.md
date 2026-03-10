# BOJ 2170 — 접근 과정: 구간 합치기

## 핵심 아이디어

선분을 **시작점 기준으로 정렬**하면, 겹치는 선분끼리 연속으로 나타난다. 정렬된 선분을 하나씩 훑으면서(sweep) 현재 구간과 합칠 수 있으면 확장, 아니면 확정하고 새 구간 시작.

## 구현

```python
segments.sort()
cur_start, cur_end = segments[0]

for s, e in segments[1:]:
    if s <= cur_end:
        cur_end = max(cur_end, e)  # 확장
    else:
        total += cur_end - cur_start  # 확정
        cur_start, cur_end = s, e

total += cur_end - cur_start  # 마지막 구간
```

## 정렬 키

`(시작점, 끝점)` 튜플로 정렬. 시작점이 같으면 끝점 순서는 결과에 영향을 주지 않지만 (어차피 `max(cur_end, e)`로 처리), 기본 튜플 비교가 자연스럽다.

## 대안으로 고려한 것

- **좌표 압축 + 배열**: 좌표를 압축한 뒤 스위프. 값 범위가 $-10^9 \sim 10^9$이므로 직접 배열은 불가능, 압축이 필요하지만 과한 설계.
- **이벤트 포인트 방식**: 각 선분의 시작/끝을 (+1, -1) 이벤트로 저장, 정렬 후 누적합. 동일 결과지만 코드가 더 복잡.

구간 합치기가 가장 직관적이고 효율적.

## I/O 최적화

$N \leq 10^6$이므로 `sys.stdin.readline`이 필수. `input()` 사용 시 TLE.
