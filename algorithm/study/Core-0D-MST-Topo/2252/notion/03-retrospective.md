# 회고

> 프로젝트: 줄 세우기
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

위상 정렬은 "의존성 해결"의 일반적 도구. 빌드 시스템, 과목 선수과목, 작업 스케줄링 등 실제 응용이 광범위하다.

## BFS vs DFS 위상 정렬

- BFS (Kahn's): 진입 차수 기반, 사이클 탐지 자연스러움
- DFS: 후위 순서의 역순, CLRS 표준 방식

이 코드에서는 BFS 방식 사용.

## 이번 프로젝트가 남긴 기준

- `줄 세우기`를 통해 `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../9372/README.md`](../../9372/README.md) (상근이의 여행)
- 다음 프로젝트: [`../../1197/README.md`](../../1197/README.md) (최소 스패닝 트리)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`topological-sort-concept.md`](../docs/concepts/topological-sort-concept.md)
