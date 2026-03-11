# 01 AWS Security Primitives

## 풀려는 문제

IAM policy 결과를 외우는 대신, 왜 allow 또는 deny가 나오는지 코드와 출력으로 설명할 수 있어야 합니다.
이 프로젝트는 가장 작은 정책 평가 규칙만 떼어 내어, 이후 least privilege 분석의 판단 기반을 만드는 데 집중합니다.

## 내가 낸 답

- policy JSON과 request JSON을 받아 statement 단위로 `Action`과 `Resource` 매칭을 평가합니다.
- `explicit deny > allow > implicit deny` 우선순위를 `Decision` 구조로 고정합니다.
- 최종 allow/deny 결과뿐 아니라 어떤 statement가 매칭되었는지까지 JSON으로 출력합니다.
- 외부 AWS API 없이 로컬 fixture와 단위 테스트만으로 재현 가능하게 유지합니다.

## 입력과 출력

- 입력: `problem/data/policy_allow_read.json`, `problem/data/request_read.json` 같은 policy/request 쌍
- 출력: `allowed`, `reason`, `matches[]` 필드를 가진 설명 가능한 decision JSON

## 검증 방법

```bash
make venv
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

## 현재 상태

- `verified`
- 로컬 fixture 기반 CLI 재현 가능
- 04번 IAM analyzer가 이 평가 감각을 전제로 확장됩니다.

## 한계와 다음 단계

- condition key, principal evaluation, policy variable은 v1 범위 밖입니다.
- 조직 전체 권한 그래프 추적은 하지 않고, 04번에서 risk finding layer를 별도로 얹습니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)
