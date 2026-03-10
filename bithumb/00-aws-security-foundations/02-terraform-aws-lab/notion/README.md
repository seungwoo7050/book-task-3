# 02 Terraform AWS Lab notion 기록

## 이 문서 묶음이 하는 일

이 `notion/`은 Terraform을 배포 성공 여부가 아니라, 보안 분석 입력을 만드는 선언형 데이터 원천으로 바라보는 기록입니다.
archive에 있던 서사형 메모는 유지하되, 현재 버전은 `verify.py`, Terraform fixture, 테스트가 실제로 보장하는 사실만 다시 묶었습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 왜 `terraform apply` 없이도 보안 학습이 가능한가?
- insecure/secure 쌍을 나누면 어떤 재현 이점이 생기는가?
- plan JSON이 왜 다음 CSPM 엔진의 직접 입력이 될 수 있는가?

## 추천 읽기 순서

학습자가 가장 빨리 손에 잡히는 재현 경로를 보려면 `05-reproduction-guide.md`를 초반에 읽는 편이 좋습니다.

1. [00-problem-framing.md](00-problem-framing.md): 문제와 경계를 먼저 확인합니다.
2. [05-reproduction-guide.md](05-reproduction-guide.md): 가장 짧은 재현 경로와 기대 결과를 확인합니다.
3. [01-approach-log.md](01-approach-log.md): 현재 구현 방향을 왜 택했는지 읽습니다.
4. [02-debug-log.md](02-debug-log.md): 어디서 자주 막히는지와 어떤 테스트가 근거인지 확인합니다.
5. [03-retrospective.md](03-retrospective.md): 지금 구현이 무엇을 증명했고 무엇을 의도적으로 비워 두었는지 읽습니다.
6. [04-knowledge-index.md](04-knowledge-index.md): 다음 프로젝트로 이어지는 개념과 근거 파일을 모아 봅니다.

## 이 버전의 근거

- 현재 문제 설명: [../problem/README.md](../problem/README.md)
- 현재 구현 안내: [../python/README.md](../python/README.md)
- 검증 코드: [../python/tests/test_terraform_lab.py](../python/tests/test_terraform_lab.py)
- 실행 스크립트: [../python/src/terraform_aws_lab/verify.py](../python/src/terraform_aws_lab/verify.py)
- Terraform insecure 예제: [../terraform/insecure/main.tf](../terraform/insecure/main.tf)
- Terraform secure 예제: [../terraform/secure/main.tf](../terraform/secure/main.tf)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
