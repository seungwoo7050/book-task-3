# 디버그 로그

> 프로젝트: 선 긋기
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 마지막 구간 누락

**증상**: 총 길이가 예상보다 짧음

**원인**: 루프가 끝난 후 마지막 구간의 길이를 더하지 않음. `for` 루프 안에서는 "새 구간이 시작될 때"만 이전 구간을 확정하므로, 마지막 구간은 루프 밖에서 처리해야 한다.

**해결**: 루프 후 `total += cur_end - cur_start` 추가

## 함정 2: 구간 확장 시 max 누락

**증상**: 포함 관계의 선분에서 길이가 짧아짐

**원인**: 겹치는 선분이 현재 구간 안에 완전히 포함될 때, `cur_end = e`로 덮어쓰면 끝점이 줄어들 수 있음. 예: 현재 (1,10)인데 (3,5)가 들어오면 cur_end가 5로 줄어듦.

**해결**: `cur_end = max(cur_end, e)` 로 확장

## 함정 3: Python TLE

**증상**: $N = 10^6$에서 시간 초과

**원인**: `input()` 사용, 또는 매번 `tuple(map(...))` 대신 리스트 컴프리헨션 미사용

**해결**: `sys.stdin.readline` + 리스트 컴프리헨션 일괄 입력

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

Python과 C++ 결과 일치.

## 왜 이 디버그 메모가 중요한가

- `선 긋기`는 `정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`interval-merge-concept.md`](../docs/concepts/interval-merge-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
