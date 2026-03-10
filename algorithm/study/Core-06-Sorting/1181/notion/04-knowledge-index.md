# 지식 인덱스

> 프로젝트: 단어 정렬
> 아래 내용은 `notion-archive/04-knowledge-index.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 개념

| 개념 | CLRS 참조 | 설명 |
|------|-----------|------|
| 다중 키 정렬 | Ch 8 | 1차: 길이, 2차: 사전순 |
| 안정 정렬 | Ch 2, 8 | 동일 키에서 원래 순서 유지 |

## 시간 복잡도

- set 구성: $O(N \cdot L)$ — $L$은 평균 단어 길이
- 정렬: $O(N \log N \cdot L)$ — 문자열 비교 비용 포함

## 연결 문제

- **BOJ 2750** (Core-06): 기본 정렬
- **BOJ 2170** (Core-06): 정렬 후 스위프
- **BOJ 11650**: 좌표 정렬 — 다중 키 정렬 변형

## 다시 연결해 볼 질문

- `단어 정렬`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?
- `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?
- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?

## 한 줄 정리 후보

- `단어 정렬`를 다시 설명할 때는 문제 이름보다 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 먼저 말한다.
- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.

## 다음 문제와 연결되는 포인트

- 앞 프로젝트: [`../../2750/README.md`](../../2750/README.md) (수 정렬하기)
- 다음 프로젝트: [`../../2170/README.md`](../../2170/README.md) (선 긋기)
- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.

## 바로 열어 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`multikey-sort-concept.md`](../docs/concepts/multikey-sort-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
