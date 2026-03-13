# 05 CSPM Rule Engine - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `scanner.py`, `cli.py`, `test_scanner.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- Terraform plan JSON과 운영 snapshot을 읽어 triage 가능한 misconfiguration finding을 어떻게 만들까
- 인프라 규칙과 계정 수명주기 규칙을 같은 finding 구조로 합칠 수 있을까

## 실제 구현 표면

- S3 public access block, open SSH/RDP ingress, storage encryption 비활성화 규칙을 plan JSON에서 바로 읽습니다.
- access key age는 별도 snapshot payload에서 읽되, 같은 `Finding` 구조로 합칩니다.
- secure fixture가 0건이어야 한다는 기준으로 false positive를 통제합니다.

## 대표 검증 엔트리

- `PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json`
- `PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../01-cloud-security-core/05-cspm-rule-engine/README.md)
2. [문제 정의](../../../01-cloud-security-core/05-cspm-rule-engine/problem/README.md)
3. [실행 진입점](../../../01-cloud-security-core/05-cspm-rule-engine/python/README.md)
4. [대표 테스트](../../../01-cloud-security-core/05-cspm-rule-engine/python/tests/test_scanner.py)
5. [핵심 구현](../../../01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/scanner.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../01-cloud-security-core/05-cspm-rule-engine/README.md)
- [problem/README.md](../../../01-cloud-security-core/05-cspm-rule-engine/problem/README.md)
- [python/README.md](../../../01-cloud-security-core/05-cspm-rule-engine/python/README.md)
- [scanner.py](../../../01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/scanner.py)
- [cli.py](../../../01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/cli.py)
- [test_scanner.py](../../../01-cloud-security-core/05-cspm-rule-engine/python/tests/test_scanner.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
