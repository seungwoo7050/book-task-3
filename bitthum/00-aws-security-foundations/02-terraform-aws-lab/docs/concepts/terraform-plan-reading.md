# Terraform Plan Reading

- CSPM 관점에서는 실제 AWS apply보다 `plan JSON`이 더 중요할 때가 많다.
- `planned_values.root_module.resources`를 읽으면 대부분의 정적 misconfiguration rule을 만들 수 있다.
- insecure/secure 예제를 둘 다 두면 rule 테스트와 데모를 쉽게 재사용할 수 있다.

