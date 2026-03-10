# 지식 인덱스

> 프로젝트: 알고리즘 수업 - 깊이 우선 탐색 1
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| DFS | Ch 22.3 | 재귀 탐색, 발견 시각(d) 기록 |
| DFS 방문 순서 | Ch 22.3 | 정점별 방문 번호 — `u.d` 타임스탬프 |

## 자료구조 사용

- **인접 리스트**: 정렬 후 결정론적 DFS 순서 보장
- **result 배열**: 1-indexed, 방문 순서 저장
- **mutable 카운터**: `order = [0]` 패턴

## 시간 복잡도

- DFS 탐색: $O(V + E)$
- 인접 리스트 정렬: $O(V \cdot d \log d)$
- 출력: $O(V)$

## 연결 문제

- **BOJ 1260** (Core-03): DFS/BFS 기본 — 이 문제의 기반
- **BOJ 24480**: DFS 방문 순서 (내림차순) — 정렬 방향만 바꿈
- **BOJ 2252** (Core-0D): 위상 정렬 — DFS finishing time 활용
- **BOJ 11724**: 연결 요소 — DFS 응용

## Python 특이사항

- `sys.setrecursionlimit(200000)`: $N \leq 100,000$ 대응
- `nonlocal` vs 리스트 래핑: 클로저에서 mutable 변수 관리
- `'\n'.join(...)`: 대량 출력 최적화

## 다시 연결해 볼 질문

- `알고리즘 수업 - 깊이 우선 탐색 1`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `알고리즘 수업 - 깊이 우선 탐색 1`를 다시 설명할 때는 문제 이름보다 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../1260/README.md`](../../1260/README.md) (DFS와 BFS)
- 다음 프로젝트: [`../../7576/README.md`](../../7576/README.md) (토마토)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`dfs-concept.md`](../docs/concepts/dfs-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
