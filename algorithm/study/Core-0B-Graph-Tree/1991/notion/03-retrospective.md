# 회고

> 프로젝트: 트리 순회
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

세 순회의 차이는 "노드 방문 시점"뿐이라는 것을 코드로 체감. `append`의 위치 하나로 전위/중위/후위가 결정된다.

## 순회의 활용

- 전위: 복사, 직렬화
- 중위: BST에서 정렬된 순서
- 후위: 삭제, 수식 트리 평가

## 딕셔너리 vs 배열

$N \leq 26$이므로 딕셔너리가 자연스럽다. 대규모라면 배열 인덱싱이 더 효율적.

## 이번 프로젝트가 남긴 기준

- `트리 순회`를 통해 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../11725/README.md`](../../11725/README.md) (트리의 부모 찾기)
- 다음 프로젝트: [`../../1167/README.md`](../../1167/README.md) (트리의 지름)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`traversal-concept.md`](../docs/concepts/traversal-concept.md)
