# 디버그 로그

> 프로젝트: 팰린드롬인지 확인하기
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 디버깅할 게 있긴 했나?

솔직히 이 문제에서 로직 버그가 날 확률은 거의 없다.
하지만 "로직은 맞는데 채점에서 틀리는" 상황은 충분히 가능하다.

## 함정 1: 개행 문자

`input()`으로 읽으면 Python이 알아서 개행을 제거하지만,
`sys.stdin.readline()`으로 읽으면 끝에 `\n`이 붙어 온다.

만약 `strip()` 없이 비교하면:
```
"level\n" != "\nlevel"  → 뒤집었을 때 "level\n"[::-1] = "\nlevel"
```
이렇게 되어서 모든 입력이 "회문이 아닌 것"으로 판별된다.

실제 solution.py에서 `.strip()`을 호출하는 이유가 바로 이것이다.

## 함정 2: 출력 형식

문제가 `1` 또는 `0`을 요구하는데, `True`/`False`나 `YES`/`NO`를 출력하면 오답이다.
이건 사소하지만 실수하면 찾기 어렵다. 출력 예제와 정확히 같은 형식을 쓰는 습관이 필요하다.

## 검증 결과

fixture 테스트(input1.txt=level→1, input2.txt=baekjoon→0)는 2/2 통과.
추가로 짝수 길이 회문 `abba`를 수동으로 넣어서 중앙 경계 처리를 확인했다.

## 왜 이 디버그 메모가 중요한가

- `팰린드롬인지 확인하기`는 `작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`palindrome-concept.md`](../docs/concepts/palindrome-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
