# 01 AWS Security Primitives evidence ledger

- 복원 원칙: 기존 blog 본문은 입력에서 제외하고 `README/problem/docs`, Python 소스, pytest, 실제 CLI 재실행만 근거로 썼다.
- 날짜 고정: 아래 실행 결과는 `2026-03-14` 기준이다.
- 프로젝트 성격: 작은 엔진이지만 이후 `04-iam-policy-analyzer`가 그대로 이어받는 판단 바닥이라는 점을 우선 확인했다.

## 사용한 입력 근거

- 설명 문서
  - `README.md`
  - `problem/README.md`
  - `python/README.md`
  - `docs/README.md`
  - `docs/concepts/iam-basics.md`
- 구현
  - `python/src/aws_security_primitives/engine.py`
  - `python/src/aws_security_primitives/cli.py`
- 테스트/fixture
  - `python/tests/test_engine.py`
  - `problem/data/policy_allow_read.json`
  - `problem/data/request_read.json`

## 다시 실행한 명령

```bash
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src \
  .venv/bin/python -m aws_security_primitives.cli \
  00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json \
  00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json

PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src \
  .venv/bin/python -m pytest \
  00-aws-security-foundations/01-aws-security-primitives/python/tests
```

- CLI 결과: `allowed: true`, `reason: at least one allow matched`, `matches[0].reason: action/resource matched`
- pytest 결과: `3 passed in 0.01s`

## 단계별 근거

### 1. statement를 같은 shape로 정규화했다

- 근거 소스: `engine.py`
- 핵심 코드: `_as_list()`, `normalized` list 구성, `_matches()`
- 확인한 사실:
  - `Statement`가 dict이든 list든 반복 가능한 같은 구조로 바꾼다.
  - `Action`과 `Resource`도 list로 강제해 `fnmatchcase()`로 wildcard 비교한다.
  - statement가 안 맞으면 `action mismatch`, `resource mismatch`를 reason 문자열로 남긴다.

### 2. precedence를 별도 합성 단계로 뒀다

- 근거 소스: `engine.py`, `test_engine.py`
- 핵심 코드: `deny_match`, `allow_match`, 최종 `Decision` return
- 확인한 사실:
  - `explicit deny`가 있으면 allow보다 먼저 최종 거부한다.
  - allow가 하나라도 있고 deny가 없으면 허용한다.
  - 둘 다 없으면 `no allow statement matched`로 끝난다.
  - 테스트는 allow, explicit deny override, no-match 세 시나리오만 고정한다.

### 3. explainability를 CLI 출력 스키마로 닫았다

- 근거 소스: `cli.py`, `python/README.md`
- 핵심 코드: `explain()` command의 JSON 직렬화
- 확인한 사실:
  - 출력은 `allowed`, `reason`, `matches[]` 세 묶음으로 고정된다.
  - `matches[]` 안에 `sid`, `effect`, `matched`, `reason`이 모두 들어간다.
  - README의 공식 재현 경로와 실제 CLI 재실행 결과가 일치한다.

## 남은 한계

- `problem/README.md`가 명시한 대로 `Condition`, `Principal`, policy variable은 다루지 않는다.
- `engine.py`는 well-formed input을 전제로 하므로 request에 `Action`/`Resource`가 없거나 policy에 `Statement`가 없으면 방어적으로 복구하지 않는다. 이 문장은 직접적인 런타임 재현 없이 소스를 읽고 적은 source-based inference다.
- least privilege finding이나 위험도 부여는 아직 없고, 그 레이어는 다음 프로젝트가 맡는다.
