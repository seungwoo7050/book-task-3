# 접근 로그

> 프로젝트: 알고리즘 수업 - 깊이 우선 탐색 1
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 1260과의 차이점

1260에서는 DFS 방문 순서를 리스트에 `append`했다. 이번에는 각 정점 $u$에 대해 `result[u] = 방문 순서`를 기록해야 한다. 리스트 순회가 아닌 **인덱스 기반 기록**이다.

## 카운터 관리 전략

Python에서 재귀 함수 내부의 카운터를 관리하는 방법이 여럿 있다:

1. **전역 변수**: `global order` — 간단하지만 함수형 스타일이 아님
2. **리스트 래핑**: `order = [0]` — mutable 객체로 클로저에서 접근 가능
3. **클래스 인스턴스**: 과한 설계

리스트 래핑 방식을 채택했다. `order[0] += 1`로 카운터를 증가시킨다.

```python
order = [0]
def dfs(u):
    order[0] += 1
    result[u] = order[0]
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            dfs(v)
```

## 인접 리스트 정렬

1260과 동일하게, "번호가 작은 정점 먼저" 조건을 위해 정렬한다. 이 패턴이 반복됨을 확인.

## 출력 최적화

$N$이 최대 100,000이므로 `print`를 $N$번 호출하면 느리다. `'\n'.join`으로 한 번에 출력하는 것이 필수.

```python
print('\n'.join(str(result[i]) for i in range(1, n + 1)))
```

## 재귀 한도

$N \leq 100,000$이므로 `sys.setrecursionlimit(200000)`을 설정했다. 1260의 10000보다 훨씬 높다. 체인 그래프에서 최대 깊이가 $N$까지 도달할 수 있기 때문이다.

## 이 접근에서 꼭 기억할 선택

- `알고리즘 수업 - 깊이 우선 탐색 1`에서 중심이 된 판단은 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`dfs-concept.md`](../docs/concepts/dfs-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
