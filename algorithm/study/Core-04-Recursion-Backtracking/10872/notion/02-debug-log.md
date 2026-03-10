# 디버그 로그

> 프로젝트: 팩토리얼
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 함정 1: 0! 처리

**증상**: $N = 0$ 입력에서 0이 출력됨

**원인**: 기저 조건을 `if n == 1`로 작성하여, $n = 0$일 때 `0 * factorial(-1) * ...`로 무한 재귀 → 결국 에러

**해결**: 기저 조건을 `if n <= 1: return 1`로 변경. $0! = 1$의 수학적 정의와 일치.

## 함정 2: 음수 입력

문제 제약상 $N \geq 0$이므로 음수는 들어오지 않지만, 기저 조건이 `n <= 1`이면 음수도 1을 반환하므로 안전하다. 방어적 코딩이 자연스럽게 이루어진 케이스.

## 확인 과정

```bash
make -C problem test
```

$N = 0, 1, 5, 10, 12$ 케이스 모두 통과.

## 왜 이 디버그 메모가 중요한가

- `팩토리얼`는 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`recursion-concept.md`](../docs/concepts/recursion-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
