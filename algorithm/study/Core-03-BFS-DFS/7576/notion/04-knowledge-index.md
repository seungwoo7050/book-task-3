# 지식 인덱스

> 프로젝트: 토마토
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 알고리즘

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| BFS | Ch 22.2 | 큐 기반 레벨 탐색 |
| 다중 소스 BFS | Ch 22.2 확장 | 가상 슈퍼 소스, 모든 소스를 초기 큐에 삽입 |
| 격자 그래프 탐색 | — | 방향 벡터 기반 이웃 탐색, 범위 검사 |

## 자료구조 사용

- **2D 리스트 (grid)**: 격자 + 방문 배열 겸용
- **deque / queue**: BFS 큐, (행, 열, 날짜) 튜플 저장
- **방향 벡터**: `dx = [0, 0, 1, -1]`, `dy = [1, -1, 0, 0]`

## 시간 복잡도

- BFS: $O(N \times M)$ — 모든 칸을 한 번씩 방문
- 불가능 판별: $O(N \times M)$ — grid 전체 순회
- 전체: $O(N \times M)$

## 연결 문제

- **BOJ 1260** (Core-03): 단일 소스 BFS — 이 문제의 기반
- **BOJ 7569**: 3차원 토마토 — 격자를 3D로 확장
- **BOJ 2178**: 미로 탐색 — 격자 BFS + 최단 거리
- **BOJ 2206**: 벽 부수기 — 격자 BFS + 상태 확장
- **BOJ 14503** (Core-05): 로봇 청소기 — 격자 시뮬레이션

## 구현 비교 (Python vs C++)

| 항목 | Python | C++ |
|------|--------|-----|
| 큐 | `collections.deque` | `std::queue` |
| I/O | `sys.stdin.readline` | `cin` + `sync_with_stdio(false)` |
| 구조 분해 | 튜플 언패킹 | structured binding (C++17) |
| 성능 | $N \times M \leq 10^6$에서 빡빡 | 여유 |

## 다시 연결해 볼 질문

- `토마토`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `토마토`를 다시 설명할 때는 문제 이름보다 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../24479/README.md`](../../24479/README.md) (알고리즘 수업 - 깊이 우선 탐색 1)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`multi-source-bfs-concept.md`](../docs/concepts/multi-source-bfs-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
