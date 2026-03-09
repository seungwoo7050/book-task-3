# 0x18 NP-Completeness Lab — 접근 과정

## Vertex Cover 검증

입력: 그래프 (정점, 간선), 인증서 (정점 부분집합)
검증: 모든 간선 $(u, v)$에 대해 $u \in S$ 또는 $v \in S$ → YES / NO

```python
cover = set(certificate)
for u, v in edges:
    if u not in cover and v not in cover:
        return "NO"
return "YES"
```

$O(E)$ 시간.

## 3-SAT 검증

입력: 절(clause) 리스트 (각 절에 리터럴 3개), 인증서 (변수 할당)
검증: 모든 절에서 최소 하나의 리터럴이 참 → YES / NO

```python
for clause in clauses:
    if not any(satisfies(lit, assignment) for lit in clause):
        return "NO"
return "YES"
```

$O(C)$ 시간 (C = 절 수).
