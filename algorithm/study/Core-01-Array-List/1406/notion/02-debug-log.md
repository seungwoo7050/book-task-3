# 디버그 로그

> 프로젝트: 에디터
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 경계 조건 처리

커서가 맨 왼쪽일 때 `L`이나 `B`가 오면 무시해야 한다.
커서가 맨 오른쪽일 때 `D`가 오면 무시해야 한다.
코드에서는 `if left:`/`if right:` 조건으로 빈 스택인지 확인하는 것으로 충분하다.

## P 명령 파싱

`P x` 형태에서 `x`를 꺼내야 한다.
`cmd = input().strip()` 후 `cmd[0] == 'P'`이면 `cmd[2]`가 삽입할 문자.
`split()` 대신 인덱스 접근을 쓴 이유는, `split()`은 공백으로 나누는 추가 연산이기 때문이다.

## sys.stdin.readline 주의

`input().strip()`에서 `strip()`을 빼먹으면 개행이 포함되어 명령 파싱이 깨진다.

## 검증 결과

fixture 테스트 통과. 수동으로 연속 L/P/B 조합도 확인.

## 왜 이 디버그 메모가 중요한가

- `에디터`는 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`editor-concept.md`](../docs/concepts/editor-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
