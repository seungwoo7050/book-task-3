# 디버그 로그

> 프로젝트: 집합의 표현
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 경로 압축 없이 TLE

$M \leq 100,000$, $N \leq 1,000,000$. 경로 압축 없으면 find가 $O(N)$이 되어 TLE.

## 함정 2: 재귀 경로 압축 → RecursionError

Python에서 재귀적 `find`는 깊은 트리에서 스택 오버플로. 반복적 path splitting 사용.

## 주의점: 출력

`sys.stdout.write` + `'\n'.join` 사용. `print` 반복은 느림.

## 확인 과정

```bash
make -C problem test
```

PASS.

## 왜 이 디버그 메모가 중요한가

- `집합의 표현`는 `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 다음 트랙에서 다시 만나게 될 선행 개념을 지금 확실히 고정해 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`disjoint-set-union.md`](../docs/concepts/disjoint-set-union.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- 같은 트랙의 큰 흐름은 [`../../README.md`](../../README.md)에서 다시 확인한다.
