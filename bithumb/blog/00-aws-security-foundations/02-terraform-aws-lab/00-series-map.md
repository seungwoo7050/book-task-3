# 02 Terraform AWS Lab 읽기 지도

Terraform을 apply 도구가 아니라 이후 보안 스캐너가 읽을 선언형 입력으로 다루게 만드는 실습이다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- 왜 Terraform lab의 핵심 산출물을 apply 결과가 아니라 plan JSON으로 봤는가?
- insecure/secure lab을 같은 검증 흐름으로 묶는 게 왜 중요했는가?
- resource type 테스트가 다음 CSPM scanner의 입력 계약 역할을 어떻게 했는가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. insecure/secure lab을 같은 검증 흐름에 묶었다: 두 Terraform 실습을 사람이 수동 비교하지 않고 같은 코드 경로로 돌릴 수 있게 만든다.
3. Phase 2. plan JSON을 산출물로 남겼다: `terraform show -json` 결과를 후속 스캐너가 읽을 실제 파일로 남긴다.
4. Phase 3. resource type 테스트로 입력 계약을 고정했다: 다음 프로젝트가 기대하는 자원 종류가 실제 plan에 들어 있는지 테스트로 확인한다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- 검증 스크립트를 “배포 자동화”가 아니라 “분석 입력 고정”으로 읽는 흐름을 강조한다.
- plan JSON 저장이 왜 다음 프로젝트와 직접 연결되는지 보여 준다.
- resource count와 resource type 테스트가 입력 계약 역할을 한다는 점으로 닫는다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): apply 없는 Terraform lab을 scan input으로 만들기

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/terraform-plan-reading.md`
- `python/src/terraform_aws_lab/verify.py`
- `python/tests/test_terraform_lab.py`
- `terraform/insecure/main.tf`
- `terraform/secure/main.tf`
