# 디버그 로그

> 프로젝트: N-Queen
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 대각선 인덱스 오프셋

**증상**: $N = 4$에서 정답(2)보다 큰 값 나옴

**원인**: `diag1` 인덱스를 `row - col`로 계산했는데, 음수 인덱스가 Python 리스트에서 뒤에서부터 접근하여 잘못된 위치를 체크

**해결**: `row - col + n - 1`로 오프셋 추가. 음수를 양수로 변환.

## 함정 2: 상태 복원 순서

**증상**: 일부 배치가 누락됨

**원인**: `col[c]`만 복원하고 대각선 배열을 복원하지 않아 이후 행에서 잘못된 충돌 감지

**해결**: 세 배열을 모두 복원. Python에서는 다중 대입이 가능: `col[c] = diag1[...] = diag2[...] = False`

## 함정 3: Python 시간 초과

**증상**: $N = 15$에서 시간 초과

**원인**: Python의 함수 호출 오버헤드가 크고, $N = 15$의 탐색 공간이 방대

**해결**: 
1. C++ 비교 구현으로 전환하여 검증
2. Python에서는 PyPy 제출로 통과 가능
3. 비트마스크 최적화로 속도 개선 가능

## C++ 디버깅

- 전역 배열 `col_used[15]`, `diag1[30]`, `diag2[30]`로 충분
- `place` 함수의 재귀 깊이 최대 $N = 15$, 스택 걱정 없음

## 확인 과정

```bash
make -C problem test          # Python PASS (작은 N)
make -C problem run-cpp       # C++ 비교 확인 (큰 N)
```

## 왜 이 디버그 메모가 중요한가

- `N-Queen`는 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`nqueen-concept.md`](../docs/concepts/nqueen-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
