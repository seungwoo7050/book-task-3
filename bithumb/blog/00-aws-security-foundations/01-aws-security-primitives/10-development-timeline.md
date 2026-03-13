# 01 AWS Security Primitives: statement match에서 explainable decision까지

IAM을 외우는 대신 결과가 어떻게 만들어지는지 설명 가능한 JSON으로 남기는 가장 작은 평가 엔진이다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "allow/deny 결과를 블랙박스가 아니라 statement-level evidence로 설명하려면 무엇이 먼저 필요했는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. statement를 단일 구조로 정규화하고 wildcard 매칭을 순수 함수로 고정했다.
2. `explicit deny > allow > implicit deny` 우선순위를 `Decision` 반환값에 박아 테스트로 잠갔다.
3. CLI가 `matches[]`까지 JSON으로 내보내게 만들어 이후 IAM analyzer의 설명 계층으로 재사용할 수 있게 했다.

## Phase 1. statement match를 순수 함수로 고정했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `statement match를 순수 함수로 고정했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: policy JSON과 request JSON을 같은 규칙으로 비교할 수 있는 최소 엔진을 세운다.
- 변경 단위: `python/src/aws_security_primitives/engine.py`의 `_as_list`, `_matches`, `StatementResult`
- 처음 가설: statement별 적용 여부와 mismatch 이유를 먼저 남기면, 최종 allow/deny 설명은 그 위에 얹기만 하면 된다.
- 실제 진행: `Statement`가 dict이든 list든 같은 리스트 구조로 정규화하고, `Action`과 `Resource`를 리스트로 강제해 wildcard 비교를 한 함수에서 처리했다. 매칭 실패도 `action mismatch`, `resource mismatch`로 분리해서 남겼다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
```

검증 신호:
- CLI가 `allowed: true`, `reason: at least one allow matched`, `matched: true`를 함께 출력했다.
- 출력 JSON 안에 `reason: action/resource matched`가 남아 “왜 붙었는지”가 bool 밖으로 나왔다.

핵심 코드:

```python
    for index, statement in enumerate(normalized, start=1):
        sid = str(statement.get("Sid", f"Statement{index}"))
        actions = _as_list(statement.get("Action", "*"))
        resources = _as_list(statement.get("Resource", "*"))
        action_match = _matches(actions, request["Action"])
        resource_match = _matches(resources, request["Resource"])
        matched = action_match and resource_match

        if matched:
            reason = "action/resource matched"
            effect = str(statement.get("Effect", "Deny"))
            if effect == "Deny":
                deny_match = True
            elif effect == "Allow":
                allow_match = True
        else:
            missing_parts: list[str] = []
            if not action_match:
                missing_parts.append("action mismatch")
            if not resource_match:
                missing_parts.append("resource mismatch")
            reason = ", ".join(missing_parts)
            effect = str(statement.get("Effect", "Deny"))
        results.append(StatementResult(sid=sid, effect=effect, matched=matched, reason=reason))
```

왜 이 코드가 중요했는가: 이 루프가 생기면서 decision 엔진은 더 이상 “맞았다/틀렸다”만 반환하지 않고, statement 하나하나를 근거로 남기기 시작했다. 이후 글 전체의 서사는 여기서 시작한다.

새로 배운 것: IAM 평가에서 중요한 첫 감각은 “statement가 적용되는가”와 “최종 decision이 무엇인가”를 분리하는 것이다. 적용 여부가 모호하면 deny precedence를 설명해도 설득력이 없다.

다음: 이제 statement 단위 결과를 모아 deny precedence를 최종 반환값에 반영해야 했다.

## Phase 2. deny precedence를 Decision에 박았다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `deny precedence를 Decision에 박았다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 매칭 결과를 모아서 실제 IAM-like 우선순위로 결론 내린다.
- 변경 단위: `python/src/aws_security_primitives/engine.py`의 최종 return 경로와 `python/tests/test_engine.py`의 deny/no-match 시나리오
- 처음 가설: allow statement 하나가 맞았더라도 더 구체적인 deny가 맞으면 그쪽이 이겨야 한다. 따라서 “첫 match wins” 같은 단순 규칙으로는 부족하다.
- 실제 진행: `deny_match`와 `allow_match`를 따로 추적해 `explicit deny`를 가장 먼저 반환하게 바꿨다. 그 다음 allow가 있으면 허용하고, 둘 다 없으면 implicit deny로 떨어지게 구성했다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

검증 신호:
- 테스트가 `3 passed in 0.01s`로 통과했고, explicit deny / no allow / allow match 세 경우가 각각 고정됐다.
- `test_explicit_deny_overrides_allow`가 secret prefix 요청에서 `explicit deny matched`를 요구했다.

핵심 코드:

```python
    if deny_match:
        return Decision(allowed=False, reason="explicit deny matched", matches=results)
    if allow_match:
        return Decision(allowed=True, reason="at least one allow matched", matches=results)
    return Decision(allowed=False, reason="no allow statement matched", matches=results)
```

왜 이 코드가 중요했는가: 결국 이 다섯 줄이 “설명 가능한 decision”의 결론부였다. 여기서 우선순위가 흐려지면 이후 least privilege 분석도 잘못된 전제를 물려받게 된다.

새로 배운 것: `explicit deny > allow > implicit deny`는 단순 암기 포인트가 아니라, 여러 statement가 동시에 맞을 때 결론을 정하는 합성 규칙이다.

다음: 이제 내부 구조를 CLI로 노출해, 로컬 fixture만으로도 판단 과정을 재현할 수 있어야 했다.

## Phase 3. CLI가 matches[]까지 드러내도록 마감했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `CLI가 matches[]까지 드러내도록 마감했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 엔진 내부의 설명을 외부 JSON 인터페이스로 고정한다.
- 변경 단위: `python/src/aws_security_primitives/cli.py`의 `explain` 커맨드
- 처음 가설: 나중에 사람이 읽든 다른 프로젝트가 이어받든, bool 하나보다는 구조화된 JSON이 훨씬 재사용 가능하다.
- 실제 진행: `Decision`과 `StatementResult`를 그대로 JSON으로 직렬화해서 `allowed`, `reason`, `matches[]`를 모두 출력하게 만들었다. README는 같은 명령을 재현 경로로 고정했고, 이후 04번 IAM analyzer가 이 설명 계층 위에 risk layer를 얹게 됐다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
$ PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

검증 신호:
- CLI 출력의 첫 줄이 바로 `allowed: true`였고, `matches` 안에 `sid`, `effect`, `matched`, `reason`이 모두 포함됐다.
- README가 같은 명령을 공식 재현 경로로 문서화했고, 실제 pytest도 그대로 통과했다.

핵심 코드:

```python
@app.command()
def explain(policy_path: Path, request_path: Path) -> None:
    policy = json.loads(policy_path.read_text())
    request = json.loads(request_path.read_text())
    decision = evaluate_policy(policy, request)
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
    typer.echo(json.dumps(output, indent=2))
```

왜 이 코드가 중요했는가: 이 직렬화 단계 덕분에 엔진의 내부 판단이 출력 스키마가 됐다. 04번 프로젝트가 `allow/deny`를 `finding`으로 바꿀 수 있었던 것도 이 설명 계층이 이미 있었기 때문이다.

새로 배운 것: Explainability는 긴 문장을 출력한다고 생기지 않는다. 어떤 근거 필드를 어떤 shape로 내보내느냐가 설명 가능성의 핵심이다.

다음: 다음 프로젝트에서는 같은 policy 입력을 “허용되는가”가 아니라 “왜 위험한가”라는 finding으로 다시 해석한다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 프로젝트는 기능적으로는 작지만, 이후 모든 보안 프로젝트의 문법을 결정했다. statement match를 근거로 남기고, precedence를 테스트로 잠그고, 마지막에 JSON 인터페이스로 내보내는 순서가 있었기 때문에 나중 단계의 analyzer와 control plane도 같은 설명 감각을 재사용할 수 있었다.
