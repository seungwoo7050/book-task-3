# 10 Route Surfaces, Case Matrix, And Demo Gateway

이 글은 프로젝트 전체에서 backend 보안이 추상적인 OWASP 용어집에서 route-level finding vocabulary로 내려오는 구간이다. 흐름은 `route surface 정의 -> case bundle 회귀 -> all-gaps demo route` 순서로 따라가는 편이 가장 자연스럽다.

## Day 1
### Session 1

- 당시 목표: backend 보안을 framework 없이도 설명 가능한 최소 surface로 자른다.
- 변경 단위: `python/src/owasp_backend_mitigations/evaluator.py`
- 처음 가설: route path와 method 정도만 있으면 finding을 설명할 수 있을 것 같았다.
- 실제 진행: path만으로는 injection, SSRF, path traversal의 차이를 말하기 어려워서 `database_touched`, `object_lookup`, `outbound_fetch`, `can_raise_debug`, `file_path_input` 같은 surface flag를 별도 필드로 올렸다.

CLI:

```bash
$ sed -n '1,220p' study/03-owasp-backend-mitigations/docs/concepts/backend-defense-five.md
$ sed -n '1,260p' study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/evaluator.py
```

검증 신호:

- 개념 문서는 injection, broken access control, SSRF, debug exposure, path traversal을 route boundary 질문으로 재구성한다.
- evaluator는 같은 다섯 질문을 `OWASP-001`부터 `OWASP-005`까지의 finding으로 고정한다.

핵심 코드:

```python
if surface.get("database_touched") and not controls["parameterized_queries"]:
    findings.append(_finding("OWASP-001", f"route={surface['route']}에서 database_touched=true인데 parameterized_queries가 없습니다"))

if surface.get("object_lookup") and not controls["ownership_scope_enforced"]:
    findings.append(_finding("OWASP-002", f"route={surface['route']}에서 ownership_scope_enforced 없이 object lookup을 수행합니다"))
```

왜 이 코드가 중요했는가:

`route=/api/v1/login`과 `route=/api/v1/users/{id}`를 둘 다 "backend endpoint"라고만 부르면 서로 다른 방어 경계가 섞여 버린다. surface flag를 먼저 고정하니 injection과 IDOR가 같은 OWASP 얘기이면서도 서로 다른 evidence를 갖는다는 사실이 분명해진다.

SSRF 쪽은 control 조합을 그대로 드러낸다.

```python
if surface.get("outbound_fetch") and (not controls["outbound_allowlist"] or not controls["private_ip_blocking"]):
    missing = [
        control
        for control, enabled in [
            ("outbound_allowlist", controls["outbound_allowlist"]),
            ("private_ip_blocking", controls["private_ip_blocking"]),
        ]
        if not enabled
    ]
    findings.append(_finding("OWASP-003", f"route={surface['route']}에 누락된 SSRF control: {', '.join(missing)}"))
```

allowlist와 private IP 차단을 같이 보는 덕분에 SSRF를 "외부 URL fetch는 위험하다"는 수준에서 멈추지 않고, 어떤 제어가 빠졌는지까지 바로 말할 수 있게 됐다.

새로 배운 것:

- OWASP를 공부할 때 가장 어려운 부분은 분류표가 아니라, 내 route가 어느 분류에 걸리는지 일상 언어로 설명하는 일이다.
- 그래서 route surface를 boolean 몇 개로 쪼개는 작업이 생각보다 훨씬 중요했다.

다음:

- 이제 이 vocabulary가 secure baseline과 negative case 묶음에서 흔들리지 않는지 확인해야 했다.

### Session 2

- 당시 목표: case bundle이 route-level finding regression suite로 동작하는지 확인한다.
- 변경 단위: `problem/data/case_bundle.json`, `python/src/owasp_backend_mitigations/cases.py`, `python/tests/test_evaluator.py`
- 처음 가설: insecure route 하나만 강하게 잡아도 학습 목적은 달성될 줄 알았다.
- 실제 진행: `secure_baseline` 1개와 negative case 5개를 분리해 false positive와 false negative를 동시에 감시하는 쪽으로 바꿨다.

CLI:

```bash
$ sed -n '1,260p' study/03-owasp-backend-mitigations/problem/data/case_bundle.json
$ PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
    .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
    study/03-owasp-backend-mitigations/problem/data/case_bundle.json
```

검증 신호:

- `secure_baseline`은 `actual_control_ids: []`로 닫히고, `raw_sql_login`, `idor_profile_read`, `webhook_ssrf`, `debug_trace_leak`, `unsafe_file_download`는 각자 하나의 control ID만 정확히 반환한다.
- CLI summary는 `passed: 6`, `failed: 0`이다.

핵심 코드:

```python
for case in manifest["cases"]:
    findings = evaluate_case(case)
    actual_control_ids = [finding["control_id"] for finding in findings]
    expected_control_ids = list(case["expected_control_ids"])
    results.append(
        {
            "name": case["name"],
            "matched": actual_control_ids == expected_control_ids,
            "actual_control_ids": actual_control_ids,
            "expected_control_ids": expected_control_ids,
            "findings": findings,
        }
    )
```

왜 이 코드가 중요했는가:

이 루프가 들어오면서 project는 "route 설명기"에서 "route 회귀 테스트"로 바뀐다. 어느 case가 어떤 finding을 내야 하는지 fixture가 먼저 말하고, evaluator는 그 기대를 맞추는 역할로 내려온다.

테스트는 각 negative case를 짧게 핀으로 꽂는다.

```python
def test_each_negative_case_returns_expected_control() -> None:
    assert case_control_ids(_case("raw_sql_login")) == ["OWASP-001"]
    assert case_control_ids(_case("idor_profile_read")) == ["OWASP-002"]
    assert case_control_ids(_case("webhook_ssrf")) == ["OWASP-003"]
    assert case_control_ids(_case("debug_trace_leak")) == ["OWASP-004"]
    assert case_control_ids(_case("unsafe_file_download")) == ["OWASP-005"]
```

case 이름과 control ID가 1:1로 붙어 있으니, route 방어 vocabulary가 의도치 않게 겹치거나 빠지는 순간 바로 드러난다.

새로 배운 것:

- secure baseline이 없는 OWASP demo는 대부분 "취약한 예시 모음"으로 끝난다.
- baseline을 같은 bundle 안에 넣어 두면 route surface의 과잉 탐지도 같이 감시할 수 있다.

다음:

- 마지막으로 모든 gap을 한 route에 몰아넣은 demo가 באמת 설명력 있는지 확인해야 했다.

## Day 2
### Session 1

- 당시 목표: 실제 코드 없이도 "이 route는 왜 위험한가"를 한 번에 보여 주는 demo endpoint를 만든다.
- 변경 단위: `problem/data/demo_profile.json`, `python/tests/test_cli.py`
- 처음 가설: demo도 bundle 안 case 중 하나를 재사용하면 충분할 것 같았다.
- 실제 진행: injection, IDOR, SSRF, debug leak, path traversal을 모두 한 번에 보이는 `/api/v1/reports/export-and-forward` route를 따로 뒀다.

CLI:

```bash
$ PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
    .venv/bin/python -m pytest study/03-owasp-backend-mitigations/python/tests
.....                                                                    [100%]
5 passed in 0.04s
```

```bash
$ PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
    .venv/bin/python -m owasp_backend_mitigations.cli demo \
    study/03-owasp-backend-mitigations/problem/data/demo_profile.json
{
  "profile": "batch_export_proxy",
  "control_ids": ["OWASP-001", "OWASP-002", "OWASP-003", "OWASP-004", "OWASP-005"]
}
```

검증 신호:

- demo route는 `database_touched`, `object_lookup`, `outbound_fetch`, `can_raise_debug`, `file_path_input`가 모두 `true`이고, 대응 control은 모두 `false`다.
- 결과적으로 다섯 finding이 한 번에 나오며, 각각 evidence에 동일 route path가 들어간다.

핵심 코드:

```python
if surface.get("can_raise_debug") and not controls["debug_stacktrace_hidden"]:
    findings.append(_finding("OWASP-004", f"route={surface['route']}에서 can_raise_debug=true인데 debug_stacktrace_hidden=false입니다"))

if surface.get("file_path_input") and not controls["safe_path_normalization"]:
    findings.append(_finding("OWASP-005", f"route={surface['route']}가 safe_path_normalization 없이 파일 경로를 입력받습니다"))
```

왜 이 코드가 중요했는가:

debug leak와 path traversal은 실제 프레임워크 예제가 없어도 evidence 문장이 충분히 구체적이다. 이 두 분기 덕분에 demo output은 단순한 `OWASP-004`, `OWASP-005` 숫자열이 아니라, "이 route에서 stacktrace를 숨기지 않았고 경로 정규화도 없다"는 review 문장으로 읽힌다.

CLI 쪽 glue는 얇다.

```python
@app.command("check-cases")
def check_cases(manifest: Path) -> None:
    result = check_case_manifest(manifest)
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
    if result["failed"]:
        raise typer.Exit(code=1)
```

evaluator와 fixture가 이미 충분히 설명 가능해서 CLI는 pretty JSON과 exit code만 담당한다. 이 얇은 CLI가 가능한 건, surface와 control contract가 이미 단단히 정리됐기 때문이다.

새로 배운 것:

- route-level security review는 실제 API 서버보다 먼저 만들어 둘 수 있다.
- 오히려 이렇게 fixture로 고정해 두면 framework를 바꿔도 어떤 control을 잃으면 안 되는지 더 또렷하게 남는다.

다음:

- 범위를 넓힌다면 XSS나 deserialization을 추가하기보다, 먼저 현재 surface schema에 새 주제를 어떻게 붙일지부터 다시 설계해야 한다.
