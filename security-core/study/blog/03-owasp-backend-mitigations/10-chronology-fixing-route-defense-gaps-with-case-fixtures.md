# route surface를 fixture로 고정하고 OWASP finding으로 읽기까지

세 번째 프로젝트에서는 auth control처럼 backend defense도 vocabulary로 바꾸려 한다. 다만 여기서는 토큰이나 세션 대신 route surface가 중심이다. 어떤 endpoint가 database를 만지는지, object lookup을 하는지, outbound fetch를 하는지, debug를 노출할 수 있는지, file path를 입력받는지가 서로 다른 방어 질문을 만든다. 이 글은 그 질문들을 `OWASP-*` finding으로 고정하고, case bundle과 composite demo로 닫는 과정을 따라간다.

## 구현 순서 요약

- `evaluator.py`에서 injection, broken access control, SSRF, debug exposure, path traversal 다섯 축을 `OWASP-001`부터 `OWASP-005`로 고정했다.
- `cases.py`에서 route fixture별 `actual_control_ids`와 `expected_control_ids`를 비교하는 summary를 만들었다.
- `cli.py`와 테스트에서 secure baseline과 composite demo가 같은 JSON surface를 쓰도록 마감했다.

## Session 1

이 프로젝트의 첫 장면은 framework가 아니라 `evaluator.py`였다. 실제 FastAPI나 Spring 앱을 띄우지 않아도 route defense를 설명할 수 있는지 보려면, 먼저 어떤 입력 표면을 볼 것인지부터 정해야 했기 때문이다. 그래서 `CONTROL_META`는 attack과 mitigation을 route 단위로 꽂아 넣는 방식으로 시작한다.

가장 설명력이 컸던 부분은 SSRF 분기였다.

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

이 조건이 중요한 이유는 SSRF를 “외부 URL을 받아서 요청한다” 정도로만 말하지 않기 때문이다. allowlist만 있어도 private IP range를 막지 않으면 내부 metadata나 lateral movement 경로가 남을 수 있고, 반대로 private IP만 막아도 승인되지 않은 외부 target으로 나가는 요청은 남는다. 무엇이 빠졌는지를 evidence 문자열로 남기는 순간, 이 프로젝트는 추상적인 보안 설명에서 route defense checklist로 바뀐다.

path traversal 분기도 같은 역할을 한다.

```python
if surface.get("file_path_input") and not controls["safe_path_normalization"]:
    findings.append(_finding("OWASP-005", f"route={surface['route']}가 safe_path_normalization 없이 파일 경로를 입력받습니다"))
```

파일 다운로드나 export endpoint는 `../` 같은 경로 조작이 쉽게 섞이기 때문에, “사용자 입력 파일 경로를 받는다”는 사실 자체가 방어 질문이 된다. 이걸 별도 finding으로 떼어 놓자 route 설계의 초점이 더 분명해졌다.

이 단계에서 다시 확인한 검증은 테스트 전체였다.

```bash
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m pytest study/03-owasp-backend-mitigations/python/tests
```

검증 신호:

- `5 passed in 0.03s`
- evaluator, case summary, CLI output shape가 한 번에 통과했다.

여기서 새로 배운 것은 backend defense를 OWASP 항목 이름으로만 읽으면 route surface와 control 경계가 약해진다는 점이었다. injection은 query structure와 맞닿고, access control은 object lookup과 맞닿으며, SSRF는 outbound fetch와 맞닿는다. surface를 먼저 잡자 mitigation도 훨씬 더 구체적으로 말할 수 있었다.

## Session 2

다음 단계는 `cases.py`였다. evaluator만 있으면 “이 route가 지금 어떤 finding을 내놓는가”는 볼 수 있어도, “이 route가 원래 어떤 finding set을 가져야 하는가”를 고정하기는 어렵다. 그래서 case bundle summary가 필요했다.

```python
def check_case_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    results: list[dict[str, Any]] = []

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

이 구조는 auth 프로젝트의 scenario summary와 닮아 보이지만, 강조점은 더 분명하게 route surface 쪽에 있다. secure baseline은 빈 리스트를 반환해야 하고, negative case는 특정 `OWASP-*` ID만 반환해야 한다. route 하나가 어느 방어를 놓쳤는지가 곧 regression contract가 된다.

실제 case bundle은 이렇게 확인했다.

```bash
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
  study/03-owasp-backend-mitigations/problem/data/case_bundle.json
```

검증 신호는 각 negative case의 mapping 자체였다.

- `passed`: `6`
- `failed`: `0`
- `raw_sql_login -> OWASP-001`
- `idor_profile_read -> OWASP-002`
- `webhook_ssrf -> OWASP-003`
- `debug_trace_leak -> OWASP-004`
- `unsafe_file_download -> OWASP-005`

이 시점에서 `docs/concepts/backend-defense-five.md`가 말하던 route 중심 읽기 방식이 실제 계약으로 굳었다. 특히 object lookup과 ownership scope를 따로 보는 방식은 “인증됐으니 읽어도 된다”는 착각을 바로 끊어 준다.

## Session 3

마지막으로 composite demo가 필요했다. negative case를 각각 나눠 두는 것만으로는 route 하나에 여러 방어 경계가 동시에 겹칠 때 어떤 모양이 되는지 보기 어렵기 때문이다. 그래서 `demo_profile.json`은 export-and-forward route 하나에 다섯 gap을 몰아 넣었다.

`cli.py`는 얇지만, 프로젝트를 닫는 entrypoint였다.

```python
@app.command("check-cases")
def check_cases(manifest: Path) -> None:
    result = check_case_manifest(manifest)
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
    if result["failed"]:
        raise typer.Exit(code=1)


@app.command()
def demo(profile: Path) -> None:
    typer.echo(json.dumps(demo_profile(profile), indent=2, ensure_ascii=False))
```

이 구조 덕분에 secure baseline과 composite demo가 같은 JSON shape를 공유한다. 개발 중에는 `check-cases`로 regression을 보고, 설명할 때는 `demo`로 한 route의 복합 위험을 읽게 된다. 학습용 surface가 한 프로젝트 안에서 자연스럽게 갈리는 셈이다.

실제 composite demo는 이렇게 남겼다.

```bash
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli demo \
  study/03-owasp-backend-mitigations/problem/data/demo_profile.json
```

판단 전환점이 된 출력은 이 조합이었다.

- `profile`: `batch_export_proxy`
- `control_ids`: `OWASP-001`, `OWASP-002`, `OWASP-003`, `OWASP-004`, `OWASP-005`
- SQL evidence: `route=/api/v1/reports/export-and-forward에서 database_touched=true인데 parameterized_queries가 없습니다`
- SSRF evidence: `outbound_allowlist, private_ip_blocking` 동시 누락
- path evidence: `safe_path_normalization 없이 파일 경로를 입력받습니다`

여기서 새로 이해한 것은 route 하나가 여러 방어 경계를 동시에 드러낼 수 있다는 점이었다. injection, SSRF, debug exposure, path traversal은 개념 문서에서는 분리돼 보이지만, 실제 endpoint 설계에서는 한 surface 위에 겹친다. composite demo가 필요한 이유가 바로 여기에 있었다.

마감은 `test_evaluator.py`와 `test_cli.py`가 했다. secure baseline 0 finding, negative case 1:1 mapping, composite demo 5 finding이 함께 고정되면서 이 프로젝트는 “OWASP 해설문”이 아니라 “route fixture 기반 defense evaluator”로 닫혔다.

## 다음

여기까지 오면 취약점 이름을 말하는 것보다 어떤 route가 어떤 방어를 놓쳤는지 말하는 편이 더 중요해진다. 다음 프로젝트 `dependency-vulnerability-workflow`는 이 감각을 patch queue 쪽으로 옮겨, 취약점 존재 여부보다 priority와 action을 먼저 계산한다.
