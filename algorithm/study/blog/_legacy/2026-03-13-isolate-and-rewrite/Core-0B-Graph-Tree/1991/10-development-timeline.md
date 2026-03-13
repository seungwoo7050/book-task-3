# BOJ 1991 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 이진 트리의 전위/중위/후위 순회 결과를 출력한다.
- 진행: 입력이 "노드 왼쪽자식 오른쪽자식" 형태로 주어진다. 자식이 없으면 `.`이다. 딕셔너리로 트리를 구성한다.
- 이슈: 루트가 항상 A라는 보장이... 있다. 문제 조건을 다시 읽었다.
- 판단: 세 순회를 각각 재귀로 구현한다. 순회 순서만 다르고 구조는 같다.

### Session 2
- 목표: 세 순회를 구현한다.

이 시점의 핵심 코드:

```python
def preorder(node):
    if node == '.':
        return
    result.append(node)
    preorder(left[node])
    preorder(right[node])
```

전위는 "방문 → 왼쪽 → 오른쪽", 중위는 "왼쪽 → 방문 → 오른쪽", 후위는 "왼쪽 → 오른쪽 → 방문". `result.append(node)` 위치만 달라진다.

CLI:

```bash
$ make -C study/Core-0B-Graph-Tree/1991/problem run-py
```

```text
ABDCEFG
DBAECFG
DBEGFCA
```

- 다음: 노드가 하나뿐인 경우 세 순회 결과가 모두 같은지 확인한다.
