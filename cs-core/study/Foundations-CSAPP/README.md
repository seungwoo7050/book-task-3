# Foundations-CSAPP

## 이 트랙이 가르치는 것

이 트랙은 CS:APP의 핵심 학습 순서를 프로젝트 중심으로 다시 정리한 것입니다.
비트 수준 사고에서 출발해 프로세서 구조와 캐시 성능의 spine을 먼저 세우고,
필요하면 역공학과 공격 모델로 확장해 들어가는 흐름을 제안합니다.

## 누구를 위한 문서인가

- CS:APP 본문을 읽고 있지만 실습 순서를 어떻게 잡아야 할지 막막한 학습자
- 각 과제가 무엇을 가르치는지 먼저 알고 시작하고 싶은 사람
- 과제 결과를 공개 저장소 형태로 정리하고 싶은 사람

## 먼저 읽을 곳

1. [`datalab/README.md`](datalab/README.md)
2. [`archlab/README.md`](archlab/README.md)
3. [`bomblab/README.md`](bomblab/README.md)
4. [`attacklab/README.md`](attacklab/README.md)
5. [`perflab/README.md`](perflab/README.md)

## 디렉터리 구조

```text
Foundations-CSAPP/
  README.md
  datalab/
  bomblab/
  attacklab/
  archlab/
  perflab/
```

## 필수 코어와 심화

- `필수 코어`: `datalab -> archlab`
- `심화/선택`: `bomblab -> attacklab`, `perflab`

CS:APP 전체를 처음 다시 정리하는 사람이라면 비트 표현과 아키텍처 spine을 먼저 끝내고,
보안/역공학과 성능 최적화는 관심 분야에 따라 확장하는 편이 더 자연스럽습니다.

## 검증 방법

2026-03-10 문서 정비 기준으로 프로젝트별 검증 방식은 다음 범주로 나뉩니다.

- 공식 공개 핸드아웃을 복원하는 프로젝트: `datalab`, `bomblab`, `attacklab`, `archlab`
- 공개 구현만으로 검증 가능한 프로젝트: `perflab`
- 각 프로젝트 README의 `problem/`, 구현 디렉터리, `docs/` README가 검증 경로를 나눠 설명합니다.

## 스포일러 경계

- `datalab`, `perflab`은 구현 원리와 검증 흐름을 비교적 자세히 설명합니다.
- `bomblab`, `attacklab`은 학습 가이드형 공개 원칙을 따릅니다.
- `archlab`은 공개 가능한 산출물과 로컬 복원 툴체인의 경계를 문서로 분리합니다.

## 포트폴리오로 확장하는 힌트

- 이 트랙을 개인 저장소로 옮길 때는 각 프로젝트에 "문제 해석", "검증", "배운 점"만 먼저 공개하고, 세부 풀이 노트는 별도 문서로 분리하는 편이 좋습니다.
- `bomblab`, `attacklab`처럼 공개 범위가 민감한 프로젝트는 이 저장소의 경계 정책을 그대로 참고하면 안전합니다.
