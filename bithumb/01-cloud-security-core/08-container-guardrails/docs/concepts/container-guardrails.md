# 컨테이너 guardrail

- EKS를 직접 띄우지 않아도 manifest 수준에서 잡아낼 수 있는 위험 설정이 많습니다.
- `hostPath`, `privileged`, `latest`, `runAsRoot`, `ALL capabilities`는 주니어도 설명하기 좋은 규칙입니다.
- manifest와 이미지 메타데이터를 함께 보면 규칙 설명이 더 구체적이 됩니다.
