# Python 내부 문서 안내

`v2-submission-polish`의 Python 문서는 최종 제출 기준에서 백엔드가 어떤 acceptance를 만족해야 하는지 정리한 내부 설계 노트다. release artifact export, regression 통과 조건, dependency health 기준을 재확인할 때 먼저 읽는다.

## 이 버전에서 중요하게 볼 내용

- 제출용 evaluator와 artifact exporter가 같은 release candidate를 바라보는지
- storage에 남는 release proof, judge score, regression 결과의 연결 방식
- dependency health와 release readiness를 어떤 규칙으로 차단하는지
- demo runbook과 backend acceptance가 문서상으로 어긋나지 않는지
