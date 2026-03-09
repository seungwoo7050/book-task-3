# Study 2 Capstone v2

`v2-submission-polish`는 `v1-regression-hardening`을 폴더 단위로 복제한 제출 마감 버전이다.

## Implemented Delta

- retrieval alias/category/risk rerank (`retrieval-v2`)
- retrieval-conditioned safe answer composer
- 같은 golden-set 기준 baseline/candidate compare artifact 재생성
- 최종 runbook, compare JSON, improvement report 반영

## Quality Result

- baseline: `v1` 코드 + `retrieval-v1`
- candidate: `v2` 코드 + `retrieval-v2`
- result: `avg_score 84.06 -> 87.76`, `critical_count 2 -> 0`, `pass_count 16 -> 19`, `fail_count 14 -> 11`

비교 artifact는 [`docs/demo/proof-artifacts`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v2-submission-polish/docs/demo/proof-artifacts)에 다시 기록했다.

## Presentation Material

- 발표용 문서는 [`docs/presentation/v2-demo-presentation.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v2-submission-polish/docs/presentation/v2-demo-presentation.md)에 정리했다.
