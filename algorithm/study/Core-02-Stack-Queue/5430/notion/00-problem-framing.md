# 문제 프레이밍

> 프로젝트: AC
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 문제를 처음 읽었을 때

BOJ 5430은 두 가지 함수를 가진 미니 언어를 시뮬레이션하는 문제다.
- **R**: 배열을 뒤집는다
- **D**: 첫 번째 원소를 삭제한다 (비어 있으면 에러)

함수 문자열이 최대 100,000자이고, 배열도 최대 100,000개다.
만약 R을 만날 때마다 진짜 배열을 뒤집으면? `reverse()`는 O(n)이니까, R이 100,000번 나오면 O(n²) = $10^{10}$.
**진짜로 뒤집으면 시간 초과다.**

이 지점에서 "뒤집기를 논리적으로만 처리해야 한다"는 발상이 나온다.

## 문제의 핵심 구조

- **입력**: $T$개 테스트 케이스, 각각 함수 문자열 $p$, 배열 크기 $n$, 배열 (JSON-like)
- **출력**: 결과 배열 또는 `error`
- **핵심**: R을 플래그로 처리하고, D는 방향에 따라 앞/뒤에서 삭제

## 왜 이 문제를 골랐는가

Core-02에서 deque의 양방향 삭제와 "실제 연산을 회피하는 논리적 트릭"을 동시에 배우는 문제다.
Gold 난이도답게, 구현이 깔끔하면서도 함정이 여럿 있다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `AC`에서 실제로 확인하려는 학습 목표는 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`deque-lazy-concept.md`](../docs/concepts/deque-lazy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../2164/README.md`](../../2164/README.md) (카드2)
