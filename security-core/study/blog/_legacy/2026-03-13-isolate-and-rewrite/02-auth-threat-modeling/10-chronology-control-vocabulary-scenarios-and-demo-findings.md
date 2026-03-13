# 10 Control Vocabulary, Scenarios, And Demo Findings

이 글은 프로젝트 전체에서 auth 설계가 "JWT를 쓰냐 안 쓰냐" 같은 기능 선택에서 `AUTH-*` finding vocabulary로 바뀌는 구간이다. 흐름은 `control meta -> scenario bundle -> hybrid demo` 순서로 잡는 편이 실제 코드와 검증 흔적을 가장 자연스럽게 따라간다.

## Day 1
### Session 1

- 당시 목표: cookie session, JWT, OAuth/OIDC 흐름을 한 evaluator에 넣되 공격면 차이를 흐리지 않는다.
- 변경 단위: `python/src/auth_threat_modeling/evaluator.py`
- 처음 가설: control ID만 리턴하면 evaluator는 충분히 작아질 것 같았다.
- 실제 진행: control ID만으로는 왜 위험한지 설명이 약해서, `CONTROL_META`에 severity, threat, recommendation을 같이 두고 evaluator는 evidence만 붙이는 구조로 정리했다.

CLI:

```bash
$ sed -n '1,220p' study/02-auth-threat-modeling/docs/concepts/session-jwt-oauth-threats.md
$ sed -n '1,260p' study/02-auth-threat-modeling/python/src/auth_threat_modeling/evaluator.py
```

검증 신호:

- 개념 문서는 cookie session의 CSRF, bearer JWT의 저장 위치와 검증, OAuth redirect flow의 `state`와 PKCE를 서로 다른 질문으로 분리한다.
- `evaluator.py`도 같은 분리를 따라 `AUTH-001`부터 `AUTH-008`까지 threat와 recommendation을 고정한다.

핵심 코드:

```python
if flow.get("oauth_enabled") and not controls["state_required"]:
    findings.append(_finding("AUTH-001", "oauth_enabled=true인데 state_required=false"))

if flow.get("oauth_enabled") and not controls["pkce_required"]:
    findings.append(_finding("AUTH-002", "oauth_enabled=true인데 pkce_required=false"))
```

왜 이 코드가 중요했는가:

OAuth를 켰을 때만 `state`와 PKCE를 묻는다는 사실이 중요하다. 그렇지 않으면 session-only 설계나 pure JWT flow에도 엉뚱한 finding이 붙는다. 이 project는 "인증 방식마다 공격면이 다르다"는 말을 분기 조건으로 보존한다.

JWT와 refresh token 쪽 분리도 같은 수준에서 고정된다.

```python
if flow.get("uses_jwt"):
    missing = [
        check
        for check, enabled in [
            ("issuer_validation", controls["issuer_validation"]),
            ("audience_validation", controls["audience_validation"]),
            ("algorithm_pinning", controls["algorithm_pinning"]),
        ]
        if not enabled
    ]
    if missing:
        findings.append(_finding("AUTH-003", "누락된 JWT 검사: " + ", ".join(missing)))
```

이 블록 덕분에 "JWT validation이 약하다"는 모호한 문장이 `issuer_validation`, `audience_validation`, `algorithm_pinning`이라는 checklist로 쪼개진다. 나중에 CLI가 주는 설명력은 여기서 나온다.

새로 배운 것:

- refresh rotation과 reuse detection은 같은 문장에 나오기 쉽지만, 실제로는 별도 control이어야 한다.
- session과 JWT를 둘 다 쓰는 hybrid flow는 공격면이 합쳐지는 게 아니라 누적된다는 점도 evaluator 분기에서 분명해졌다.

다음:

- 이제 이 control vocabulary가 fixture 묶음 위에서 실제로 안정적으로 동작하는지 확인해야 했다.

### Session 2

- 당시 목표: secure baseline과 negative scenario를 한 번에 돌려 `AUTH-*` finding이 흔들리지 않는지 확인한다.
- 변경 단위: `python/src/auth_threat_modeling/scenarios.py`, `problem/data/scenario_bundle.json`, `python/tests/test_evaluator.py`
- 처음 가설: insecure scenario 하나만 있어도 evaluator를 설명할 수 있을 것 같았다.
- 실제 진행: baseline 1개와 negative case 4개를 분리해 `control gap -> expected_control_ids` 매핑을 더 선명하게 만들었다.

CLI:

```bash
$ sed -n '1,260p' study/02-auth-threat-modeling/problem/data/scenario_bundle.json
$ PYTHONPATH=study/02-auth-threat-modeling/python/src \
    .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
    study/02-auth-threat-modeling/problem/data/scenario_bundle.json
```

검증 신호:

- `secure_baseline`은 빈 finding이어야 하고, 실제 출력도 `actual_control_ids: []`로 닫힌다.
- `oauth_missing_state_and_pkce`는 `AUTH-001`, `AUTH-002`, `jwt_validation_gap`은 `AUTH-003`, `AUTH-004`, `AUTH-005`만 정확히 반환한다.
- CLI summary는 `passed: 5`, `failed: 0`이다.

핵심 코드:

```python
for scenario in manifest["scenarios"]:
    findings = evaluate_scenario(scenario)
    actual_control_ids = [finding["control_id"] for finding in findings]
    expected_control_ids = list(scenario["expected_control_ids"])
    results.append(
        {
            "name": scenario["name"],
            "matched": actual_control_ids == expected_control_ids,
            "actual_control_ids": actual_control_ids,
            "expected_control_ids": expected_control_ids,
            "findings": findings,
        }
    )
```

왜 이 코드가 중요했는가:

evaluator만 있으면 "finding을 만들 수 있다"까지는 말할 수 있다. 하지만 이 루프가 들어오면서 프로젝트는 "fixture가 기대한 finding만 만든다"까지 증명한다. auth threat modeling을 학습 자료가 아니라 regression 가능한 lab으로 만든 지점이다.

테스트도 같은 방향으로 얇고 정확하게 붙는다.

```python
def test_oauth_missing_state_and_pkce_returns_expected_controls() -> None:
    assert scenario_control_ids(_scenario("oauth_missing_state_and_pkce")) == ["AUTH-001", "AUTH-002"]


def test_recovery_and_rate_limit_gap_returns_expected_controls() -> None:
    assert scenario_control_ids(_scenario("recovery_and_rate_limit_gap")) == ["AUTH-007", "AUTH-008"]
```

negative case를 한 줄 assertion으로 잘게 나눈 덕분에, 어느 control이 흔들렸는지 바로 드러난다. `secure_baseline`과 같이 놓여 있으니 false positive도 같이 감시할 수 있다.

새로 배운 것:

- threat model evaluator는 "취약한 예시를 많이 모으는 일"보다 secure baseline을 잃지 않는 일이 더 중요하다.
- `actual_control_ids == expected_control_ids` 비교가 있어야 finding 순서까지 포함한 vocabulary가 안정된다.

다음:

- 마지막으로 이 evaluator가 혼합 auth rollout 하나를 설명하는 demo에서도 충분히 읽히는지 확인해야 했다.

## Day 2
### Session 1

- 당시 목표: 복합 auth 설계를 한 번에 보여 주는 demo profile이 실제 review 언어로 읽히는지 확인한다.
- 변경 단위: `problem/data/demo_profile.json`, `python/src/auth_threat_modeling/scenarios.py`, `python/tests/test_cli.py`
- 처음 가설: demo는 scenario bundle의 한 항목을 그대로 재사용해도 될 것 같았다.
- 실제 진행: hybrid flow 특성을 더 잘 보이기 위해 cookie mutation, JWT, OAuth, recovery code를 모두 켠 `oidc_cookie_hybrid_demo`를 별도 profile로 뒀다.

CLI:

```bash
$ PYTHONPATH=study/02-auth-threat-modeling/python/src \
    .venv/bin/python -m pytest study/02-auth-threat-modeling/python/tests
........                                                                 [100%]
8 passed in 0.04s
```

```bash
$ PYTHONPATH=study/02-auth-threat-modeling/python/src \
    .venv/bin/python -m auth_threat_modeling.cli demo \
    study/02-auth-threat-modeling/problem/data/demo_profile.json
{
  "profile": "oidc_cookie_hybrid_demo",
  "control_ids": ["AUTH-001", "AUTH-003", "AUTH-004", "AUTH-005", "AUTH-006", "AUTH-007", "AUTH-008"]
}
```

검증 신호:

- demo는 `AUTH-002`를 일부러 포함하지 않는다. `pkce_required`는 `true`라서 PKCE는 이미 만족하기 때문이다.
- 대신 `state_required=false`, `audience_validation=false`, `reuse_detection=false`, `csrf_protection=false`, `recovery_codes_hashed=false`, `rate_limit_mode=none`이 모두 finding으로 살아난다.

핵심 코드:

```python
storage_reasons: list[str] = []
if controls["token_storage"] in {"localStorage", "sessionStorage", "url"}:
    storage_reasons.append(f"token_storage={controls['token_storage']}")
if int(controls["access_ttl_minutes"]) > 15:
    storage_reasons.append(f"access_ttl_minutes={controls['access_ttl_minutes']}")
if storage_reasons:
    findings.append(_finding("AUTH-004", ", ".join(storage_reasons)))
```

왜 이 코드가 중요했는가:

`AUTH-004`는 "token을 어디에 저장했는가"와 "TTL을 얼마나 길게 줬는가"를 같이 본다. demo profile에서 `localStorage`와 `20분 TTL`이 동시에 evidence로 찍히는 이유도 여기 있다. storage와 lifetime을 같이 봐야 탈취 피해 규모를 설명할 수 있다는 판단이 코드에 남아 있다.

demo 쪽 glue는 아주 얇다.

```python
def demo_profile(path: Path) -> dict[str, Any]:
    profile = load_json(path)
    findings = evaluate_scenario(profile)
    return {
        "profile": profile["name"],
        "control_ids": [finding["control_id"] for finding in findings],
        "findings": findings,
    }
```

이 얇은 함수가 의미 있는 건, 앞선 scenario evaluator가 이미 충분히 설명 가능한 finding을 만든다는 뜻이기 때문이다. demo가 별도 로직을 많이 요구하지 않는다는 사실 자체가 evaluator 설계가 잘 닫혔다는 신호였다.

새로 배운 것:

- auth threat modeling은 OAuth나 JWT 자체를 구현하지 않아도, control gap vocabulary만 안정적으로 잡히면 충분히 학습 가치가 크다.
- 특히 hybrid auth는 "기능이 많아서 복잡하다"보다 "누락 control이 누적돼서 review가 길어진다"는 사실을 demo가 잘 보여 줬다.

다음:

- 범위를 넓힐 때도 provider 연동부터 들어가기보다 WebAuthn, device trust, risk-based auth를 이런 vocabulary 방식으로 먼저 쪼갤 수 있을지부터 따져 보는 편이 맞다.
