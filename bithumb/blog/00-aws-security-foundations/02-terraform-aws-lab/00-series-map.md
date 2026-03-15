# 02 Terraform AWS Lab series map

이 시리즈는 `02-terraform-aws-lab`을 "Terraform 기초 실습"이 아니라, 이후 CSPM rule engine이 믿고 읽을 수 있는 plan JSON 입력을 만드는 프로젝트로 읽는다. 핵심은 apply가 아니라 `insecure`와 `secure` 예제를 같은 절차로 재생산하고, 그 결과를 `tfplan.json`으로 남기고, 어떤 resource type이 들어 있어야 하는지 테스트로 잠가 두는 데 있다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   insecure/secure fixture 쌍을 어떻게 scan input으로 바꾸고, 그 입력 계약을 어떻게 테스트로 고정했는지 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 왜 Terraform의 핵심 산출물을 apply 결과가 아니라 plan JSON으로 봐야 했는가
- insecure/secure 두 lab을 같은 검증 루프로 묶는 일이 왜 중요한가
- 이 lab이 다음 CSPM scanner에게 정확히 무엇을 넘겨주고, 무엇은 아직 맡지 않는가
