# 디버그 로그

> 프로젝트: AC
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 빈 배열 파싱

`n=0`일 때 입력이 `[]`이다.
`"[]"[1:-1].split(',')` → `['']` (길이 1, 빈 문자열 원소).
이걸 deque에 넣으면 빈 문자열 원소가 하나 들어간다.
해결: `n == 0`이면 `deque()`로 빈 deque 생성.

## D 후 error 처리

`D`를 만났을 때 deque가 비어 있으면 즉시 `error`를 출력하고 나머지 명령을 건너뛰어야 한다.
`break`로 루프를 빠져나온 뒤 `error` 플래그를 확인한다.

## 출력 행 줄바꿈

`print()` 사용 시 자동 개행이 포함되므로 별도 처리 불필요.
다만 deque 원소가 문자열이므로 `','.join(dq)`으로 직접 결합 가능.

## 검증 결과
fixture 테스트 통과. Python/C++ 교차 검증 완료.

## 왜 이 디버그 메모가 중요한가

- `AC`는 `명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`deque-lazy-concept.md`](../docs/concepts/deque-lazy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
