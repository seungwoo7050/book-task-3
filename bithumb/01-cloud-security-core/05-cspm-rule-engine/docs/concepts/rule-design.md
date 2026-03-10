# CSPM 규칙 설계

- 좋은 rule은 설명 가능해야 하고, 왜 발동했는지 운영자가 바로 이해할 수 있어야 합니다.
- false positive를 줄이려면 rule 입력 스키마를 좁히는 편이 좋습니다.
- Terraform plan과 운영 snapshot을 섞어 보면 CSPM이 정적 분석에만 머물지 않는다는 감각을 얻을 수 있습니다.
