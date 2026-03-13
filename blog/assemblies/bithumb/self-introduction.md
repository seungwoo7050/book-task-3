# Bithumb 자소서

저는 보안 문제를 볼 때도 개별 규칙을 얼마나 많이 만들었는지보다, 그 규칙들이 실제 운영 흐름 안에서 어떻게 연결되는지가 더 중요하다고 생각합니다. `bithumb` 트랙은 그 기준으로 정리한 결과물입니다.

대표 capstone인 `Cloud Security Control Plane`에서는 Terraform plan, IAM policy, CloudTrail fixture, Kubernetes manifest를 finding 파이프라인으로 통합하고, exception, remediation dry-run, report까지 한 흐름으로 연결했습니다. 덕분에 기능 나열보다 운영 판단과 근거를 먼저 보는 습관을 더 분명하게 만들 수 있었습니다.

공통 코어와 `backend-common` 경험도 이 제출본의 바닥이 됐습니다. 42서울과 FastAPI 기준선에서 쌓은 인증/인가, API 경계, 검증 구조 감각이 있었기 때문에 보안/운영 문제도 더 구조적으로 바라볼 수 있었습니다.

협업에서도 finding과 exception, remediation 근거를 분리해 남기면 팀이 더 명확한 기준 위에서 결정할 수 있다고 생각합니다. 저는 이런 기준을 코드와 문서로 함께 남기는 사람이 되고 싶습니다.

입사 후에도 운영과 보안 관점을 분리하지 않고, 구조와 검증 근거를 함께 남기는 방식으로 기여하고 싶습니다.
