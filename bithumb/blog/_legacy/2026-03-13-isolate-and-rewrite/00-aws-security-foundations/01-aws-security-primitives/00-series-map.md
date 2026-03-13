# 01 AWS Security Primitives - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `engine.py`, `cli.py`, `test_engine.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- IAM policy를 외우지 않고, 왜 allow 또는 deny가 나오는지 어떤 최소 규칙으로 설명할 수 있을까
- 후속 least privilege 분석 전에 statement 매칭 결과를 어떤 구조로 남겨야 할까

## 실제 구현 표면

- policy JSON과 request JSON을 받아 최종 `allowed`와 `reason`을 계산합니다.
- statement별 `matched` 여부와 `action mismatch`, `resource mismatch`를 `matches[]`에 남깁니다.
- `explicit deny > allow > implicit deny` 우선순위를 코드와 CLI 출력에서 바로 확인할 수 있습니다.

## 대표 검증 엔트리

- `PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json`
- `PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../00-aws-security-foundations/01-aws-security-primitives/README.md)
2. [문제 정의](../../../00-aws-security-foundations/01-aws-security-primitives/problem/README.md)
3. [실행 진입점](../../../00-aws-security-foundations/01-aws-security-primitives/python/README.md)
4. [대표 테스트](../../../00-aws-security-foundations/01-aws-security-primitives/python/tests/test_engine.py)
5. [핵심 구현](../../../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../00-aws-security-foundations/01-aws-security-primitives/README.md)
- [problem/README.md](../../../00-aws-security-foundations/01-aws-security-primitives/problem/README.md)
- [python/README.md](../../../00-aws-security-foundations/01-aws-security-primitives/python/README.md)
- [engine.py](../../../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py)
- [cli.py](../../../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/cli.py)
- [test_engine.py](../../../00-aws-security-foundations/01-aws-security-primitives/python/tests/test_engine.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
