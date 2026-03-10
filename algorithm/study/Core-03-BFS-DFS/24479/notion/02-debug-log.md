# 디버그 로그

> 프로젝트: 알고리즘 수업 - 깊이 우선 탐색 1
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 재귀 한도 부족

**증상**: 큰 입력에서 `RecursionError: maximum recursion depth exceeded`

**원인**: 기본 재귀 한도 1000으로는 $N = 100,000$인 체인 그래프를 처리할 수 없다.

**해결**: `sys.setrecursionlimit(200000)` 설정. $N$의 2배로 여유를 둔다.

## 함정 2: 비방문 정점 처리

**증상**: 비연결 그래프에서 일부 정점의 방문 순서가 쓰레기 값으로 출력

**원인**: `result` 배열을 초기화하지 않아 메모리의 잔여값이 출력됨

**해결**: `result = [0] * (n + 1)`로 0 초기화. 문제 정의상 미방문 정점은 0을 출력해야 하므로, 0 초기화가 곧 기본값이다.

## 함정 3: 출력 속도

**증상**: 로직은 맞지만 시간 초과 (TLE)

**원인**: `for i in range(1, n+1): print(result[i])`로 매번 `print` 호출

**해결**: `'\n'.join(...)` 으로 문자열을 한 번에 구성 후 단일 `print` 호출.

## 확인 과정

`make -C problem test`로 검증. 연결 그래프, 비연결 그래프, 단일 정점 케이스 모두 통과.

## 왜 이 디버그 메모가 중요한가

- `알고리즘 수업 - 깊이 우선 탐색 1`는 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`dfs-concept.md`](../docs/concepts/dfs-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
