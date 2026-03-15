# 05 CSPM Rule Engine series map

이 시리즈는 `05-cspm-rule-engine`을 Terraform plan lint가 아니라, plan과 운영 snapshot을 같은 finding 언어로 묶는 첫 multi-source scanner로 읽는다. 실제 규칙은 S3 public access(`CSPM-001`), open SSH/RDP ingress(`CSPM-002`), storage encryption off(`CSPM-003`), access key age(`CSPM-004`) 네 가지다. 반대로 nested module traversal, drift detection, 조직 단위 inventory 수집은 아직 하지 않는다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   plan resource dispatch에서 시작해 snapshot rule을 더하고, secure plan 0건과 combined CLI의 차이를 어떻게 읽어야 하는지 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 왜 CSPM을 plan-only parser가 아니라 multi-source finding engine으로 봐야 하는가
- insecure plan과 aged access key snapshot은 어떤 finding 조합으로 드러나는가
- secure plan이 깨끗하다는 말과 전체 입력 묶음이 깨끗하다는 말은 왜 다른가
