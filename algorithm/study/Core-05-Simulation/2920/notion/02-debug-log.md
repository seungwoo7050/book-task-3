# 디버그 로그

> 프로젝트: 음계
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 특이사항

이 문제는 로직이 단순해서 디버깅할 것이 거의 없었다.

## 유일한 주의점: 출력 형식

**증상**: 대소문자 또는 철자 오류로 오답 처리

**원인**: `Ascending`이 아니라 `ascending`, `Descending`이 아니라 `descending`으로 소문자 출력이 필요

**해결**: 문제 원문에서 출력 형식을 정확히 확인하고 소문자로 출력

## 확인 과정

```bash
make -C problem test
```

모든 fixture 통과.

## 왜 이 디버그 메모가 중요한가

- `음계`는 `복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`simulation-concept.md`](../docs/concepts/simulation-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
