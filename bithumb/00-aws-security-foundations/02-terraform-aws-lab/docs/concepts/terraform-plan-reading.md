# Terraform plan 읽기

- CSPM 관점에서는 실제 AWS apply보다 `plan JSON`이 더 중요한 입력일 때가 많습니다.
- `planned_values.root_module.resources` 구조를 읽을 수 있으면 많은 정적 규칙을 만들 수 있습니다.
- insecure/secure 예제를 함께 유지하면 테스트와 데모 재사용성이 좋아집니다.
