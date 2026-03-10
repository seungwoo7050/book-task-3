# 디버그 로그

> 프로젝트: 키로거
> 아래 내용은 `notion-archive/02-debug-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 성능 이슈

처음에 `print()`로 출력했을 때, 대량 테스트 케이스에서 미세하게 느렸다.
`sys.stdout.write()`로 바꾸니 안정적으로 통과했다.
Python에서 대량 출력이 필요할 때는 `sys.stdout.write`가 관용적 선택이다.

## 빈 스택 체크

1406과 동일하게, `<`/`-`에서 left가 비어 있으면 무시, `>`에서 right가 비어 있으면 무시.
`if left:` 가드로 충분하다.

## 검증 결과

fixture 테스트 통과. Python/C++ 교차 검증 완료.

## 왜 이 디버그 메모가 중요한가

- `키로거`는 `순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.
- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.

## 다음 수정 때 다시 볼 체크리스트

- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?
- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?
- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?

## 같이 점검할 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`keylogger-concept.md`](../docs/concepts/keylogger-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
