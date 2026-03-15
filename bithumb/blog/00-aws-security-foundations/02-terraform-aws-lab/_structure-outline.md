# 02 Terraform AWS Lab structure outline

## 중심 질문

- 이 lab이 왜 "Terraform을 써 봤다"가 아니라 "분석 입력을 만들었다"는 이야기로 읽혀야 하는지
- insecure/secure 차이를 사람이 아니라 다음 scanner가 읽을 수 있게 고정하려면 무엇이 먼저 필요했는지

## 글 흐름

1. insecure/secure 예제가 어떤 보안 차이를 대표하는지로 시작한다.
2. `verify.py`가 두 lab을 같은 Terraform 절차로 재생산하는 장면을 두 번째 축으로 둔다.
3. `tfplan.json` 저장을 산출물 전환점으로 설명한다.
4. resource-type 테스트와 병렬 state lock 메모로 입력 계약의 실제 성격을 마무리한다.

## 반드시 남길 증거

- `verify.py`의 `terraform_available`, `run_lab`, `json_path.write_text`
- `test_terraform_lab.py`의 resource type assertion
- insecure/secure `main.tf`와 `tfplan.json`의 public access / ingress / IAM policy 차이
- `2026-03-14` verify 출력 `insecure: 5 resources`, `secure: 5 resources`
- `2026-03-14` pytest `3 passed in 11.35s`
- `2026-03-14` 병렬 검증 시 `Error acquiring the state lock`

## 반드시 피할 서술

- "Terraform 배포 실습"처럼 읽히는 설명
- resource count만 말하고 실제 보안 차이를 숨기는 문장
- 병렬 실행 충돌을 무시한 채 verifier가 완전히 견고한 것처럼 쓰는 서술
- rule evaluation까지 이미 이 lab이 한다고 오해하게 만드는 표현

## 톤 체크

- chronology는 `fixture 차이 -> 재현 루프 -> plan JSON -> 테스트 계약` 순서로 살아 있어야 한다.
- 홍보문보다 "어떤 입력을 다음 프로젝트에 넘겨주는가"와 "어디서 아직 충돌할 수 있는가"가 함께 읽혀야 한다.
