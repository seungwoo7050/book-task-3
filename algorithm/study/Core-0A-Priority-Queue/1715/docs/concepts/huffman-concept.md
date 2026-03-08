# 카드 합치기 개념 정리 — 허프만 코딩 패턴

## CLRS 연결
CLRS Ch 16.3 Huffman Codes — 최소 비용의 이진 트리 구축.
카드 합치기는 허프만 알고리즘과 동일한 구조.

## 핵심 아이디어
매번 가장 작은 두 묶음을 합치면 총 비교 횟수가 최소.
→ **최소 힙**으로 항상 최솟값 2개를 $O(\log N)$에 추출.

## 알고리즘
```
while heap.size > 1:
    a = extract_min()
    b = extract_min()
    total += a + b
    insert(a + b)
```

## 시간 복잡도
$N-1$번 합치기 × 각 $O(\log N)$ = $O(N \log N)$.
