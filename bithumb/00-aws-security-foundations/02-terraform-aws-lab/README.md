# 02 Terraform AWS Lab

## 프로젝트 한줄 소개

Terraform을 배포 도구가 아니라 보안 분석 입력으로 읽는 실습입니다.

## 왜 배우는가

CSPM 규칙 엔진은 결국 Terraform plan JSON 같은 선언형 입력을 읽어야 합니다. 이 프로젝트는 apply 없이도 안전한 설정과 위험한 설정의 차이를 해석하는 감각을 만드는 데 초점을 둡니다.

## 현재 구현 범위

- insecure/secure Terraform 예제를 비교합니다.
- plan JSON을 생성하고 후속 프로젝트에서 재사용할 입력 형태를 정리합니다.
- AWS 계정 없이도 로컬 검증 중심으로 실습합니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify
```

## 검증 명령

```bash
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

Terraform 코드를 얼마나 길게 썼는지보다, 어떤 설정 차이를 어떻게 검증했고 왜 그 차이가 중요한지 설명하는 쪽이 포트폴리오 품질을 더 높입니다.

## 알려진 한계

- 실제 apply는 하지 않습니다.
- v1은 plan JSON을 읽고 비교하는 단계까지만 다룹니다.
