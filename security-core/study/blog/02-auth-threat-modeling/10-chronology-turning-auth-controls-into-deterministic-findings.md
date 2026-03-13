# auth 방식을 설명하지 않고 control gap을 고정하기까지

두 번째 프로젝트로 넘어오면 질문이 달라진다. 이제는 hash와 MAC처럼 primitive를 나누는 대신, session cookie, bearer JWT, OAuth/OIDC redirect flow를 어떻게 서로 다른 공격면으로 읽을 것인가가 핵심이 된다. 이 프로젝트는 실제 provider나 login server를 띄우지 않는다. 대신 `AUTH-*` control vocabulary를 먼저 세우고, scenario bundle과 demo profile이 그 vocabulary를 반복 가능한 finding으로 바꾸는 흐름을 만든다.

## 구현 순서 요약

- `evaluator.py`에서 `AUTH-001`부터 `AUTH-008`까지 threat, recommendation, evidence 규칙을 먼저 고정했다.
- `scenarios.py`에서 scenario bundle을 읽어 `actual_control_ids`와 `expected_control_ids`를 비교하는 summary를 만들었다.
- `cli.py`와 테스트에서 secure baseline 0 finding과 hybrid demo 다중 finding을 같은 JSON 계약으로 마감했다.

## Session 1

처음 손댄 곳은 `evaluator.py`였다. auth를 “JWT를 쓴다”, “OAuth를 붙인다”처럼 기술 선택으로만 말하면, 무엇이 빠졌을 때 어떤 공격면이 열리는지 설명이 금방 약해진다. 그래서 이 프로젝트는 기능 이름보다 통제 이름을 먼저 붙이는 쪽으로 갔다.

`CONTROL_META`는 그 출발점이다. `AUTH-001`은 `state`, `AUTH-002`는 `PKCE`, `AUTH-003`은 JWT issuer/audience/algorithm validation, `AUTH-004`는 token storage와 access TTL, `AUTH-005`는 refresh rotation과 reuse detection, `AUTH-006`은 cookie mutation과 CSRF, `AUTH-007`은 recovery code hashing, `AUTH-008`은 rate limiting을 맡는다. 이렇게 vocabulary를 먼저 고정해 두지 않으면, 나중에 scenario를 늘려도 설명은 금방 “이번엔 이런 문제가 있다”는 식으로 흐려진다.

특히 JWT와 refresh token 분기가 전환점이었다.

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

JWT를 쓰는 순간 단순히 “서명을 본다”에서 끝나지 않는다는 점이 코드에 바로 남는다. issuer, audience, allowed algorithm을 함께 묶어야 한다는 사실이 이 한 블록에서 드러난다. 이 프로젝트가 `exp` 자체를 별도 필드로 모델링하지 않더라도 `access_ttl_minutes`를 따로 보는 이유도 같다. 검증 누락과 탈취 피해 확산은 다른 질문이기 때문이다.

```python
if flow.get("uses_refresh_token"):
    missing_refresh = [
        check
        for check, enabled in [
            ("refresh_rotation", controls["refresh_rotation"]),
            ("reuse_detection", controls["reuse_detection"]),
        ]
        if not enabled
    ]
    if missing_refresh:
        findings.append(_finding("AUTH-005", "누락된 refresh control: " + ", ".join(missing_refresh)))
```

여기서 처음 더 분명해진 개념은 `rotation`과 `reuse detection`이 같은 통제가 아니라는 점이었다. rotation은 새 refresh token을 발급하는 정책이고, reuse detection은 탈취된 이전 token이 다시 쓰였을 때 그 재사용을 이상 징후로 잡는 정책이다. 둘 중 하나만 있어도 설명은 반쪽짜리가 된다.

이 시점에서 다시 돌린 검증은 패키지 테스트 전체였다.

```bash
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m pytest study/02-auth-threat-modeling/python/tests
```

검증 신호:

- `8 passed in 0.04s`
- evaluator, scenario summary, CLI shape가 함께 통과했다.

여기서 또렷해진 것은 cookie, JWT, OAuth가 이름만 다른 같은 인증 방식이 아니라는 사실이었다. cookie session은 브라우저 자동 전송 때문에 CSRF가 중요하고, bearer JWT는 저장 위치와 validation 누락이 중요하며, redirect-based OAuth는 `state`와 PKCE가 핵심이다.

## Session 2

control vocabulary만으로는 아직 프로젝트가 닫히지 않았다. 어떤 시나리오가 어떤 finding set을 가져야 하는지 반복 가능하게 비교해야 했다. 그 역할을 맡은 곳이 `scenarios.py`였다.

```python
def check_scenarios_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    results: list[dict[str, Any]] = []

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

핵심은 `matched`가 구현 세부를 비교하는 값이 아니라 vocabulary 계약을 비교한다는 점이다. secure baseline은 빈 리스트를 돌려줘야 하고, 특정 negative scenario는 예상한 control ID만 돌려줘야 한다. 그래야 이 프로젝트가 “auth 개념 정리”가 아니라 “control gap evaluator”가 된다.

scenario bundle은 실제로 이렇게 확인했다.

```bash
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
  study/02-auth-threat-modeling/problem/data/scenario_bundle.json
```

출력에서 중요한 검증 신호는 각 scenario의 조합 그 자체였다.

- `passed`: `5`
- `failed`: `0`
- `secure_baseline -> []`
- `oauth_missing_state_and_pkce -> AUTH-001, AUTH-002`
- `jwt_validation_gap -> AUTH-003, AUTH-004, AUTH-005`
- `cookie_without_csrf -> AUTH-006`
- `recovery_and_rate_limit_gap -> AUTH-007, AUTH-008`

이 시점에서 `docs/concepts/session-jwt-oauth-threats.md`가 하던 말이 코드와 출력으로 단단해졌다. 시나리오별 `expected_control_ids`를 잡아 둔 덕분에, 설명문보다 회귀 검증이 먼저 생긴 셈이었다.

## Session 3

마지막으로 필요한 것은 사람이 한 번에 읽을 수 있는 demo였다. secure baseline과 negative scenario 묶음만 있으면 개발자는 테스트를 통과시킬 수 있지만, 학습자는 “한 설계에서 어떤 control이 동시에 빠지는가”를 바로 보기 어렵다. 그래서 `demo_profile()`과 CLI output을 따로 열었다.

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

demo는 얇은 래퍼처럼 보여도 역할이 분명하다. bundle summary가 “여러 시나리오가 각자 맞는가”를 보는 층이라면, demo는 “한 설계가 어떤 구멍을 동시에 드러내는가”를 읽는 층이다. 그래서 baseline과 다중 finding demo가 함께 있어야 이 프로젝트의 설명력이 살아난다.

실제 demo는 이렇게 확인했다.

```bash
PYTHONPATH=study/02-auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli demo \
  study/02-auth-threat-modeling/problem/data/demo_profile.json
```

이 출력이 남긴 검증 신호는 다음과 같았다.

- `profile`: `oidc_cookie_hybrid_demo`
- `control_ids`: `AUTH-001`, `AUTH-003`, `AUTH-004`, `AUTH-005`, `AUTH-006`, `AUTH-007`, `AUTH-008`
- `AUTH-001 evidence`: `oauth_enabled=true인데 state_required=false`
- `AUTH-003 evidence`: `누락된 JWT 검사: audience_validation`
- `AUTH-004 evidence`: `token_storage=localStorage, access_ttl_minutes=20`
- `AUTH-005 evidence`: `누락된 refresh control: reuse_detection`

여기서 다시 분명해진 것은 auth surface마다 걱정하는 축이 다르다는 사실이었다. `state`는 redirect request/response를 묶는 통제고, PKCE는 authorization code 탈취 재사용을 어렵게 만드는 통제다. cookie mutation과 CSRF 보호가 auth 방식의 일부로 같이 나오는 것도 이 demo에서는 자연스럽게 읽힌다.

마감은 `test_cli.py`와 `test_evaluator.py`가 했다. secure baseline 0 finding과 hybrid demo 다중 finding을 둘 다 테스트로 고정했기 때문에, 이 프로젝트는 문장 감각보다 output contract가 앞서는 형태로 닫혔다.

## 다음

이 프로젝트가 만든 것은 auth 개념 요약문이 아니라 control gap을 반복 실행 가능한 finding으로 바꾸는 습관이었다. 다음 글 `owasp-backend-mitigations`는 이 습관을 route surface로 옮겨, backend defense를 `OWASP-*` vocabulary로 다시 고정한다.
