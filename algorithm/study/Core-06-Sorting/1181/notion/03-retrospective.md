# 회고

> 프로젝트: 단어 정렬
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

Python의 `sorted(key=...)`는 다중 키 정렬을 매우 간결하게 구현할 수 있게 한다. 튜플 키를 반환하면 자동으로 다단계 비교가 이루어진다. 이 패턴은 정렬이 필요한 거의 모든 Python 문제에서 재사용된다.

## set의 활용

중복 제거에 `set`을 쓰는 것은 자연스럽지만, `set`은 **순서가 없다**는 점을 기억해야 한다. 중복 제거 후 정렬하는 순서가 중요하다: `sorted(set(...))`이지 `set(sorted(...))`이 아님.

## 안정 정렬의 가치

Python의 Timsort는 **안정 정렬**이다. 같은 길이의 단어들 사이에서 원래 순서가 유지될 수 있다. 하지만 이 문제에서는 사전순 비교를 명시적으로 하므로 안정성에 의존할 필요가 없다.

## 이번 프로젝트가 남긴 기준

- `단어 정렬`를 통해 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../2750/README.md`](../../2750/README.md) (수 정렬하기)
- 다음 프로젝트: [`../../2170/README.md`](../../2170/README.md) (선 긋기)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`multikey-sort-concept.md`](../docs/concepts/multikey-sort-concept.md)
