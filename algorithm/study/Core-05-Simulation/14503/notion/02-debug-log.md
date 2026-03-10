# 디버그 로그

> 프로젝트: 로봇 청소기
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 왼쪽 회전 방향 오류

**증상**: 로봇이 오른쪽으로 회전함

**원인**: `(d + 1) % 4`를 사용 — 이것은 오른쪽 회전 (시계 방향)

**해결**: `(d + 3) % 4` 또는 `(d - 1) % 4` 사용 — 왼쪽 회전 (반시계 방향)

## 함정 2: 후진 시 청소된 칸도 벽으로 판정

**증상**: 후진 가능한데 멈춰버림

**원인**: 후진 조건에서 `grid[br][bc] == 0 and not cleaned[br][bc]`로 검사. 청소된 빈 칸으로도 후진할 수 있는데, 미청소 빈 칸만 허용함.

**해결**: 후진 조건은 `grid[br][bc] != 1` (벽이 아니면 됨). 청소 여부와 무관하게 빈 칸이면 후진 가능.

## 함정 3: 현재 칸 중복 청소

**증상**: 청소 횟수가 예상보다 많음

**원인**: 루프 시작 때마다 무조건 `count += 1`

**해결**: `if not cleaned[r][c]` 조건으로 이미 청소된 칸은 건너뜀

## 확인 과정

```bash
make -C problem test
make -C problem run-py
make -C problem run-cpp
```

Python과 C++ 결과 일치 확인.

## 왜 이 디버그 메모가 중요한가

- `로봇 청소기`는 `복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`robot-concept.md`](../docs/concepts/robot-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
