# 디버그 로그

> 프로젝트: 공유기 설치
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 정렬 누락

**증상**: 판별 함수가 잘못된 결과 반환

**원인**: 집 좌표가 정렬되어 있지 않으면 탐욕적 판별이 성립하지 않음

**해결**: 입력 후 `houses.sort()` 필수

## 함정 2: 이진 탐색 범위

**증상**: 답이 0이나 음수로 나옴

**원인**: `lo = 0`으로 시작하면 `d = 0`이 feasible로 판정되어 의미 없는 답

**해결**: `lo = 1` (최소 거리는 1 이상)

## 함정 3: ans 갱신 시점

**증상**: feasible한 최대 d를 놓침

**원인**: 마지막 feasible한 mid를 기록하지 않음

**해결**: `if feasible(mid): ans = mid` 로 갱신하고, `lo = mid + 1`로 더 큰 값 탐색

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

Python과 C++ 결과 일치. PASS.

## 왜 이 디버그 메모가 중요한가

- `공유기 설치`는 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`parametric-search-concept.md`](../docs/concepts/parametric-search-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
