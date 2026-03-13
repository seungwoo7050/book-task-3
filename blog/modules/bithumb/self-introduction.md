# Bithumb 자소서 Module

저는 보안 문제를 볼 때도 개별 규칙을 얼마나 많이 만들었는지보다, 그 규칙들이 실제 운영 흐름 안에서 어떻게 연결되는지가 더 중요하다고 생각합니다. `bithumb` 트랙은 그 기준으로 정리한 결과물입니다.

대표 capstone인 `Cloud Security Control Plane`에서는 Terraform plan, IAM policy, CloudTrail fixture, Kubernetes manifest를 finding 파이프라인으로 통합하고, exception, remediation dry-run, report까지 한 흐름으로 연결했습니다. 덕분에 기능 나열보다 운영 판단과 근거를 먼저 보는 습관을 더 분명히 만들 수 있었습니다.

제가 이 모듈을 중요하게 생각하는 이유는 백엔드나 플랫폼 역할에서도 결국 운영 기준과 위험 판단을 함께 봐야 하기 때문입니다. 어떤 위험을 발견했고, 어떤 조치를 안전하게 제안하는지 설명할 수 있어야 한다고 생각합니다.

협업에서도 이런 태도는 그대로 이어집니다. finding과 exception, remediation 근거를 분리해 남기면 팀이 더 명확한 기준 위에서 결정할 수 있습니다.

입사 후에도 운영과 보안 관점을 분리하지 않고, 구조와 검증 근거를 함께 남기는 방식으로 기여하고 싶습니다.
