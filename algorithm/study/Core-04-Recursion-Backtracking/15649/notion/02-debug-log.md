# 디버그 로그

> 프로젝트: N과 M (1)
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 상태 복원 누락

**증상**: 첫 번째 순열만 올바르고, 이후 결과가 비어 있음

**원인**: `used[i] = False` (되돌림)를 빠뜨려서, 첫 번째 DFS 경로 이후 모든 숫자가 "사용 중"으로 남음

**해결**: 재귀 호출 직후 `seq.pop()` + `used[i] = False`를 반드시 쌍으로 작성

## 함정 2: 출력 형식

**증상**: 숫자가 붙어서 출력됨 (e.g., "12" instead of "1 2")

**원인**: `print(seq)` → 리스트 형태로 출력

**해결**: `' '.join(map(str, seq))`로 공백 구분 출력

## 함정 3: depth vs length 혼동

**증상**: 순열 길이가 맞지 않음

**원인**: depth를 1부터 시작하면서 종료 조건을 `depth == m`으로 설정 → 길이 $m-1$의 순열 생성

**해결**: depth를 0부터 시작하고, `depth == m`에서 종료. 또는 1부터 시작하고 `depth > m`에서 종료.

## 확인 과정

```bash
make -C problem test
```

$N = 4, M = 2$ 등 여러 케이스 통과 확인.

## 왜 이 디버그 메모가 중요한가

- `N과 M (1)`는 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`backtracking-concept.md`](../docs/concepts/backtracking-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
