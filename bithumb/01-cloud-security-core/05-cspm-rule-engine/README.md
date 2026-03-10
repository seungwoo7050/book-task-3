# 05 CSPM Rule Engine

## 프로젝트 한줄 소개

Terraform plan JSON과 운영 snapshot을 읽어 triage 가능한 finding을 만드는 규칙 엔진입니다.

## 왜 배우는가

CSPM은 결국 “이 설정이 안전한가?”에 자동으로 답하는 도구입니다. 이 프로젝트는 Terraform plan과 access key snapshot을 함께 읽어, 오탐을 줄이면서도 설명 가능한 규칙을 만드는 감각을 익히게 합니다.

## 현재 구현 범위

- Terraform plan JSON misconfiguration을 탐지합니다.
- S3 public access, open ingress, storage encryption, access key age를 검사합니다.
- 운영자가 바로 triage할 수 있는 finding 형태로 결과를 반환합니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
```

## 검증 명령

```bash
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

규칙 개수보다 규칙의 근거와 false positive를 어떻게 줄였는지를 보여 주는 편이 더 낫습니다. secure fixture에서 finding 0개가 나오는 이유까지 설명하면 좋습니다.

## 알려진 한계

- v1 rule set은 S3, Security Group, encryption, access key age로 제한합니다.
- 실제 배포 환경 전체를 스캔하지 않고 로컬 fixture 입력만 사용합니다.
