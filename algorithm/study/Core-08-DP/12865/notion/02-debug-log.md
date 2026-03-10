# 디버그 로그

> 프로젝트: 평범한 배낭
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 순방향 순회 오류

**증상**: 같은 아이템이 여러 번 포함되어 가치가 비정상적으로 높음

**원인**: `for j in range(w, K+1)` (순방향)으로 순회하면, `dp[j-w]`가 이미 현재 아이템을 포함한 값일 수 있음

**해결**: `for j in range(K, w-1, -1)` (역방향)으로 변경

## 함정 2: dp 배열 크기

**증상**: IndexError

**원인**: `dp = [0] * K` — 인덱스 K에 접근 불가

**해결**: `dp = [0] * (K + 1)` — 0부터 K까지 K+1개

## 함정 3: 무게가 용량 초과

**증상**: 음수 인덱스 접근

**원인**: `j - w`가 0 미만이 될 때 범위 검사 없음

**해결**: `range(K, w-1, -1)` — `j >= w`일 때만 순회하므로 자연스럽게 해결

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

Python과 C++ 결과 일치. PASS.

## 왜 이 디버그 메모가 중요한가

- `평범한 배낭`는 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`knapsack-concept.md`](../docs/concepts/knapsack-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
