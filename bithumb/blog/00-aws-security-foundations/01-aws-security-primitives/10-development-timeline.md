# 01 AWS Security Primitives: IAM을 외우는 대신 "왜 이런 decision이 나왔는가"를 먼저 고정한 가장 작은 엔진

이 프로젝트는 기능적으로는 작다. AWS 계정을 붙이지도 않고, policy language 전체를 구현하지도 않는다. 대신 `problem/README.md`가 요구한 아주 좁은 질문 하나, 즉 "`Effect`, `Action`, `Resource`, explicit deny가 최종 decision에 어떤 순서로 반영되는가"를 코드와 출력으로 설명하는 데 집중한다. `2026-03-14`에 CLI와 pytest를 다시 돌려 보니, 이 프로젝트의 가치는 기능 양이 아니라 이후 analyzer들이 가져다 쓸 판단 문법을 얼마나 깔끔하게 고정했는가에 있었다.

## Step 1. 먼저 statement match 자체를 근거로 남기게 만들었다

처음부터 allow/deny 결론으로 바로 가면 나중에 "왜 그 결론이 나왔는가"를 되짚기 어려워진다. `engine.py`가 먼저 한 일은 statement를 비교 가능한 같은 shape로 바꾸고, match 여부를 `StatementResult`로 남기는 것이었다.

`evaluate_policy()`는 두 가지 정규화를 먼저 수행한다.

- `Statement`가 dict이면 list 한 개로 감싼다.
- `Action`, `Resource`가 scalar든 list든 `_as_list()`로 리스트화한다.

그 다음 `_matches()`에서 `fnmatchcase()`를 써 wildcard를 처리하고, action과 resource가 모두 맞아야 `matched = true`가 된다. 맞지 않으면 `action mismatch`, `resource mismatch`를 reason으로 남긴다. 즉 이 엔진은 처음부터 "결과"보다 "근거"를 쌓는 방식으로 시작한다.

이 판단은 `2026-03-14` CLI 재실행에서도 그대로 드러났다.

```bash
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src \
  .venv/bin/python -m aws_security_primitives.cli \
  00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json \
  00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
```

출력은 단순 `allowed: true`로 끝나지 않았다. `matches[0]` 안에 `sid: AllowRead`, `matched: true`, `reason: action/resource matched`가 함께 들어 있었다. 작은 프로젝트지만, 이 시점부터 이미 "explainable decision"의 모양이 만들어진 셈이다.

## Step 2. 그 위에 explicit deny precedence를 별도 합성 규칙으로 올렸다

statement match를 남겼다고 IAM-like decision이 완성되는 건 아니다. 여러 statement가 동시에 맞을 수 있을 때 어떤 결론이 이기는지가 더 중요하다. 이 프로젝트는 그 결론 합성 규칙을 `deny_match`와 `allow_match` 두 플래그로 명시적으로 분리했다.

`engine.py`의 마지막 분기는 단순하지만, 이후 프로젝트 전체에 가장 오래 남는 규칙이다.

```python
if deny_match:
    return Decision(allowed=False, reason="explicit deny matched", matches=results)
if allow_match:
    return Decision(allowed=True, reason="at least one allow matched", matches=results)
return Decision(allowed=False, reason="no allow statement matched", matches=results)
```

이 규칙은 `2026-03-14` pytest 재실행으로 다시 확인했다.

```bash
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src \
  .venv/bin/python -m pytest \
  00-aws-security-foundations/01-aws-security-primitives/python/tests
```

결과는 `3 passed in 0.01s`였다. 하지만 더 중요한 건 통과 숫자보다 시나리오다.

- allow match
- explicit deny overrides allow
- no allow statement matched

즉 이 엔진은 "정상 허용"만 검증하지 않고, 실제로 가장 헷갈리기 쉬운 deny precedence와 no-match fallthrough를 함께 잠근다. 이후 `04-iam-policy-analyzer`가 broad permission을 위험 finding으로 바꿀 수 있는 것도, 여기서 이미 허용/거부 합성 규칙이 흔들리지 않기 때문이다.

## Step 3. 마지막으로 CLI를 출력 스키마로 고정했다

이 프로젝트가 단순 유틸리티를 넘어 트랙의 첫 기반이 되는 이유는 CLI가 엔진 내부 판단을 그대로 구조화된 JSON으로 내보내기 때문이다. `cli.py`는 `evaluate_policy()`의 결과를 받아 `allowed`, `reason`, `matches[]`를 그대로 직렬화한다.

```python
output = {
    "allowed": decision.allowed,
    "reason": decision.reason,
    "matches": [
        {
            "sid": match.sid,
            "effect": match.effect,
            "matched": match.matched,
            "reason": match.reason,
        }
        for match in decision.matches
    ],
}
```

이 출력 스키마 덕분에 이 프로젝트는 두 가지 역할을 동시에 한다.

- 사람이 IAM 결과를 "왜 그런지" 읽는 입문 엔진
- 다음 프로젝트가 재사용할 수 있는 설명 계층

README가 강조한 "최종 allow/deny 결과뿐 아니라 어떤 statement가 매칭되었는지까지 JSON으로 출력"한다는 문장은 실제 소스와 `2026-03-14` CLI 출력에서 그대로 확인됐다. 여기서 explainability는 긴 문장을 쓰는 일이 아니라, 어떤 필드를 어떤 모양으로 고정하는가의 문제라는 점이 분명해진다.

## Step 4. 작지만 일부러 남긴 바깥 경계도 분명하다

문서를 좋게 쓰려면 이 프로젝트를 과하게 키우지 않는 것도 중요하다. `problem/README.md`와 `docs/concepts/iam-basics.md`는 둘 다 범위를 아주 좁게 둔다.

- `Condition` 제외
- `Principal` 제외
- policy variable 제외
- 실제 AWS API 조회 제외

소스도 그 선택을 그대로 따른다. `evaluate_policy()`는 well-formed input을 가정하고 `request["Action"]`, `request["Resource"]`, `policy["Statement"]`에 바로 접근한다. 따라서 malformed JSON을 친절하게 복구하는 엔진은 아니다. 이건 결함이라기보다 이 단계에서 "정책 평가 감각"만 먼저 배우겠다는 의도적 축소에 가깝다. 이 문장은 소스만 보고 적은 source-based inference다.

## 정리

`01-aws-security-primitives`는 작지만 가볍지 않다. statement match를 먼저 근거로 남기고, 그 위에 deny precedence를 얹고, 마지막에 JSON explainability로 닫는 순서가 이후 IAM analyzer와 control plane의 설명 방식까지 결정한다. 즉 이 프로젝트의 성취는 AWS를 많이 흉내 낸 데 있지 않고, "왜 허용되었고 왜 거부되었는가"를 가장 작은 형태로 흔들리지 않게 고정한 데 있다.
