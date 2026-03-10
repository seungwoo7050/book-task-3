# v2 제출 마감 버전

`v2-submission-polish`는 `v1-regression-hardening`을 바탕으로 retrieval 개선, compare artifact 재생성, 최종 runbook과 발표 자료까지 정리한 제출 마감 버전이다. 이 트랙에서 학생이 가장 먼저 참고해야 할 최종 capstone snapshot이다.

## 이번 버전에서 달라진 점

- retrieval alias/category/risk rerank (`retrieval-v2`)
- retrieval-conditioned safe answer composer
- 같은 golden-set 기준 baseline/candidate compare artifact 재생성
- 최종 runbook, compare JSON, improvement report 반영

## 품질 결과

- baseline: `v1` 코드 + `retrieval-v1`
- candidate: `v2` 코드 + `retrieval-v2`
- 결과: `avg_score 84.06 -> 87.76`, `critical_count 2 -> 0`, `pass_count 16 -> 19`, `fail_count 14 -> 11`

## 먼저 볼 문서

- [`problem/README.md`](./problem/README.md)
- [`docs/README.md`](./docs/README.md)
- [`docs/demo/demo-runbook.md`](./docs/demo/demo-runbook.md)
- [`docs/presentation/v2-demo-presentation.md`](./docs/presentation/v2-demo-presentation.md)

## 현재 상태

- 비교 artifact는 [`docs/demo/proof-artifacts`](./docs/demo/proof-artifacts/)에 다시 기록돼 있다.
- 학생 입장에서는 "개선 실험을 어떻게 증빙으로 마감하는가"를 보기 가장 좋은 버전이다.
