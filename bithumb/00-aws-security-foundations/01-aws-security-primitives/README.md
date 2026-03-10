# 01 AWS Security Primitives

## 프로젝트 한줄 소개

IAM 정책이 왜 허용되거나 거부되는지 설명하는 가장 작은 평가 엔진입니다.

## 왜 배우는가

IAM 문법을 아는 것과 평가 흐름을 설명하는 것은 다릅니다. 이 프로젝트는 `Effect`, `Action`, `Resource`, `explicit deny`를 코드로 체감하게 만들어 이후 least privilege 분석의 출발점이 됩니다.

## 현재 구현 범위

- policy JSON과 request JSON을 입력으로 받습니다.
- statement별 매칭 결과와 최종 허용/거부 결정을 설명합니다.
- wildcard action/resource matching과 explicit deny 우선순위를 다룹니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli explain 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
```

## 검증 명령

```bash
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

허용/거부 결과만 보여 주지 말고, 왜 그런 결정이 났는지 statement 단위 설명을 함께 제시하면 포트폴리오 설득력이 크게 올라갑니다.

## 알려진 한계

- condition keys, principal evaluation, policy variables는 v1 범위 밖입니다.
- 실제 AWS API를 호출하지 않고 로컬 fixture만 사용합니다.
