# 회고

> 프로젝트: 타임머신
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

벨만-포드의 핵심은 "V-1번이면 충분"과 "V번째 갱신 = 음의 사이클". 이 두 성질의 증명을 이해하면 알고리즘이 자연스럽다.

## 최단 경로 알고리즘 비교

| 알고리즘 | 음의 가중치 | 음의 사이클 | 시간 |
|----------|:-----------:|:-----------:|------|
| BFS | × | × | $O(V+E)$ |
| 다익스트라 | × | × | $O((V+E)\log V)$ |
| 벨만-포드 | ○ | 탐지 | $O(VE)$ |
| 플로이드-워셜 | ○ | 탐지 | $O(V^3)$ |

## 이번 프로젝트가 남긴 기준

- `타임머신`를 통해 `가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../1753/README.md`](../../1753/README.md) (최단경로)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`bellman-ford-concept.md`](../docs/concepts/bellman-ford-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
