# 04 IAM Policy Analyzer

## 프로젝트 한줄 소개

IAM 정책을 읽고 least privilege 관점의 finding으로 바꾸는 분석기입니다.

## 왜 배우는가

정책 평가 엔진만으로는 “허용된다/거부된다”까지만 말할 수 있습니다. 이 프로젝트는 그 위에 위험 설명을 얹어, broad permission과 privilege escalation 패턴을 triage 가능한 finding으로 바꾸는 연습을 합니다.

## 현재 구현 범위

- broad admin과 scoped policy를 구분합니다.
- `iam:PassRole` 같은 escalation action을 별도 고위험 finding으로 분리합니다.
- 설명 가능한 finding 구조와 severity를 반환합니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
```

## 검증 명령

```bash
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

정책이 위험하다는 결론만 적기보다, 어떤 패턴을 어떤 근거로 finding으로 만들었는지 예시 JSON과 함께 설명하면 훨씬 설득력 있습니다.

## 알려진 한계

- SCP, permission boundary, condition-based privilege narrowing은 v1 범위 밖입니다.
- 조직 전체의 권한 그래프까지 추적하지는 않습니다.
