# 회고

> 프로젝트: 토마토
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

다중 소스 BFS는 단일 소스 BFS와 코드가 거의 동일하다. 차이는 오직 "초기 큐에 무엇을 넣느냐"뿐이다. 이 단순한 확장이 "여러 곳에서 동시에 퍼지는 현상"을 정확히 모델링한다는 것이 인상적이었다.

## 격자 BFS의 패턴

이 문제에서 확립한 격자 BFS 패턴은 이후 많은 문제에서 반복된다:
1. 방향 벡터 `dx, dy` 정의
2. 범위 검사 `0 <= nx < N and 0 <= ny < M`
3. 조건 검사 후 큐에 추가
4. grid 자체를 visited로 활용 가능

## Python vs C++ 비교

Python 구현과 C++ 구현을 모두 유지했다. Gold 문제에서 $N, M \leq 1000$이면 격자 크기가 $10^6$까지 가능하고, Python에서는 시간 제한이 빡빡할 수 있다. C++ 구현은 `ios_base::sync_with_stdio(false)`와 `cin.tie(nullptr)`로 I/O를 최적화했다.

## "가상 슈퍼 소스" 아이디어

CLRS의 개념적 설명(가상 소스에서 모든 실제 소스로 0-가중치 간선)은 다중 소스 BFS뿐 아니라 다중 소스 최단 경로(Dijkstra)에도 적용된다. Core-0C의 최단 경로 문제에서 이 아이디어가 재등장할 수 있다.

## 만약 다시 풀다면

3차원 격자 확장(BOJ 7569)을 바로 시도할 것이다. `dz = [0, 0, 0, 0, 1, -1]`만 추가하면 된다. 패턴의 확장성을 확인하는 좋은 연습이다.

## 이번 프로젝트가 남긴 기준

- `토마토`를 통해 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../24479/README.md`](../../24479/README.md) (알고리즘 수업 - 깊이 우선 탐색 1)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`multi-source-bfs-concept.md`](../docs/concepts/multi-source-bfs-concept.md)
