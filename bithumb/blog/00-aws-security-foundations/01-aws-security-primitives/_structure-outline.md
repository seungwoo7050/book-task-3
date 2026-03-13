# 01 AWS Security Primitives 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- IAM decision을 거대한 서비스 모사가 아니라 `statement match -> deny precedence -> explainable JSON` 순서로 고정하는 작은 엔진으로 읽는다.
- 최종 본문은 `05-evidence-ledger.md`를 그대로 압축하지 않고, 각 phase가 왜 다음 phase를 부르는지 드러내는 흐름으로 배치한다.

## 먼저 붙들 소스 묶음
- [`../../../00-aws-security-foundations/01-aws-security-primitives/README.md`](../../../00-aws-security-foundations/01-aws-security-primitives/README.md)
- [`../../../00-aws-security-foundations/01-aws-security-primitives/problem/README.md`](../../../00-aws-security-foundations/01-aws-security-primitives/problem/README.md)
- [`../../../00-aws-security-foundations/01-aws-security-primitives/docs/concepts/iam-basics.md`](../../../00-aws-security-foundations/01-aws-security-primitives/docs/concepts/iam-basics.md)
- [`../../../00-aws-security-foundations/01-aws-security-primitives/python/README.md`](../../../00-aws-security-foundations/01-aws-security-primitives/python/README.md)
- [`../../../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py`](../../../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py)
- [`../../../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/cli.py`](../../../00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/cli.py)
- [`../../../00-aws-security-foundations/01-aws-security-primitives/python/tests/test_engine.py`](../../../00-aws-security-foundations/01-aws-security-primitives/python/tests/test_engine.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - 프로젝트 질문, source set, canonical verify를 먼저 고정한다.
- `10-development-timeline.md`
  - 도입: 왜 IAM을 “허용/거부”보다 “설명 가능한 decision”으로 읽는지 잡는다.
  - Phase 1. statement match를 순수 함수로 고정했다.
  - Phase 2. deny precedence를 `Decision`에 박았다.
  - Phase 3. CLI가 `matches[]`까지 드러내도록 마감했다.
  - 마무리: 다음 프로젝트가 이 explainability 계층을 어떻게 finding으로 확장하는지 질문으로 넘긴다.

## 강조할 코드와 CLI
- 코드 앵커: `_matches`, `StatementResult`, deny precedence return, CLI JSON 직렬화
- CLI 앵커: `python -m aws_security_primitives.cli ...`, `pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests`
- 개념 훅: IAM에서 “statement 적용 여부”와 “최종 decision”은 같은 층위가 아니라는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.
