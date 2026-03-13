# 01 AWS Security Primitives 근거 정리

IAM을 외우는 대신 결과가 어떻게 만들어지는지 설명 가능한 JSON으로 남기는 가장 작은 평가 엔진이다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. statement match를 순수 함수로 고정했다

이 구간에서는 `statement match를 순수 함수로 고정했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: policy JSON과 request JSON을 같은 규칙으로 비교할 수 있는 최소 엔진을 세운다.
- 변경 단위: `python/src/aws_security_primitives/engine.py`의 `_as_list`, `_matches`, `StatementResult`
- 처음 가설: statement별 적용 여부와 mismatch 이유를 먼저 남기면, 최종 allow/deny 설명은 그 위에 얹기만 하면 된다.
- 실제 조치: `Statement`가 dict이든 list든 같은 리스트 구조로 정규화하고, `Action`과 `Resource`를 리스트로 강제해 wildcard 비교를 한 함수에서 처리했다. 매칭 실패도 `action mismatch`, `resource mismatch`로 분리해서 남겼다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json`
- 검증 신호:
  - CLI가 `allowed: true`, `reason: at least one allow matched`, `matched: true`를 함께 출력했다.
  - 출력 JSON 안에 `reason: action/resource matched`가 남아 “왜 붙었는지”가 bool 밖으로 나왔다.
- 핵심 코드 앵커: `00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py:45-68`
- 새로 배운 것: IAM 평가에서 중요한 첫 감각은 “statement가 적용되는가”와 “최종 decision이 무엇인가”를 분리하는 것이다. 적용 여부가 모호하면 deny precedence를 설명해도 설득력이 없다.
- 다음: 이제 statement 단위 결과를 모아 deny precedence를 최종 반환값에 반영해야 했다.

## Phase 2. deny precedence를 Decision에 박았다

이 구간에서는 `deny precedence를 Decision에 박았다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: 매칭 결과를 모아서 실제 IAM-like 우선순위로 결론 내린다.
- 변경 단위: `python/src/aws_security_primitives/engine.py`의 최종 return 경로와 `python/tests/test_engine.py`의 deny/no-match 시나리오
- 처음 가설: allow statement 하나가 맞았더라도 더 구체적인 deny가 맞으면 그쪽이 이겨야 한다. 따라서 “첫 match wins” 같은 단순 규칙으로는 부족하다.
- 실제 조치: `deny_match`와 `allow_match`를 따로 추적해 `explicit deny`를 가장 먼저 반환하게 바꿨다. 그 다음 allow가 있으면 허용하고, 둘 다 없으면 implicit deny로 떨어지게 구성했다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests`
- 검증 신호:
  - 테스트가 `3 passed in 0.01s`로 통과했고, explicit deny / no allow / allow match 세 경우가 각각 고정됐다.
  - `test_explicit_deny_overrides_allow`가 secret prefix 요청에서 `explicit deny matched`를 요구했다.
- 핵심 코드 앵커: `00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py:70-74`
- 새로 배운 것: `explicit deny > allow > implicit deny`는 단순 암기 포인트가 아니라, 여러 statement가 동시에 맞을 때 결론을 정하는 합성 규칙이다.
- 다음: 이제 내부 구조를 CLI로 노출해, 로컬 fixture만으로도 판단 과정을 재현할 수 있어야 했다.

## Phase 3. CLI가 matches[]까지 드러내도록 마감했다

이 구간에서는 `CLI가 matches[]까지 드러내도록 마감했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: 엔진 내부의 설명을 외부 JSON 인터페이스로 고정한다.
- 변경 단위: `python/src/aws_security_primitives/cli.py`의 `explain` 커맨드
- 처음 가설: 나중에 사람이 읽든 다른 프로젝트가 이어받든, bool 하나보다는 구조화된 JSON이 훨씬 재사용 가능하다.
- 실제 조치: `Decision`과 `StatementResult`를 그대로 JSON으로 직렬화해서 `allowed`, `reason`, `matches[]`를 모두 출력하게 만들었다. README는 같은 명령을 재현 경로로 고정했고, 이후 04번 IAM analyzer가 이 설명 계층 위에 risk layer를 얹게 됐다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json`
  - `PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests`
- 검증 신호:
  - CLI 출력의 첫 줄이 바로 `allowed: true`였고, `matches` 안에 `sid`, `effect`, `matched`, `reason`이 모두 포함됐다.
  - README가 같은 명령을 공식 재현 경로로 문서화했고, 실제 pytest도 그대로 통과했다.
- 핵심 코드 앵커: `00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/cli.py:13-31`
- 새로 배운 것: Explainability는 긴 문장을 출력한다고 생기지 않는다. 어떤 근거 필드를 어떤 shape로 내보내느냐가 설명 가능성의 핵심이다.
- 다음: 다음 프로젝트에서는 같은 policy 입력을 “허용되는가”가 아니라 “왜 위험한가”라는 finding으로 다시 해석한다.
