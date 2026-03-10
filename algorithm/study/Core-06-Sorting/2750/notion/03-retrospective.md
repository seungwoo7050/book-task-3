# 회고

> 프로젝트: 수 정렬하기
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

Python의 내장 `sort()`는 Timsort 알고리즘으로, 최악 $O(N \log N)$, 부분 정렬된 데이터에서 $O(N)$까지 내려간다. 실전에서는 이 내장 정렬이 거의 항상 최선의 선택이다.

## 정렬의 하한

비교 기반 정렬의 하한은 $\Omega(N \log N)$ (CLRS Ch 8.1 결정 트리 논증). 이보다 빠른 정렬(계수/기수/버킷)은 입력에 대한 가정이 필요하다.

## 다음 단계

1181에서 "다중 키 정렬" (길이 → 사전순), 2170에서 "정렬 후 스위프"라는 응용으로 확장.

## 이번 프로젝트가 남긴 기준

- `수 정렬하기`를 통해 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 다음 프로젝트: [`../../1181/README.md`](../../1181/README.md) (단어 정렬)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`sorting-concept.md`](../docs/concepts/sorting-concept.md)
