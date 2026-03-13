# 10 Reusing Foundation Vocabulary In One Review

이 글은 capstone 전체에서 foundations 프로젝트의 질문을 하나의 review bundle로 다시 모으는 구간이다. 흐름은 `local evaluator 재구성 -> bundle 결합 -> consolidated review 출력` 순서로 따라가는 편이 자연스럽다.

## Day 1
### Session 1

- 당시 목표: foundation 프로젝트를 import하지 않으면서도 같은 control ID와 priority vocabulary를 유지한다.
- 변경 단위: `python/src/collab_saas_security_review/crypto.py`, `auth.py`, `backend.py`, `dependency.py`
- 처음 가설: foundations 패키지를 그대로 import해 재사용하는 편이 더 간단할 것 같았다.
- 실제 진행: capstone README가 "앞선 foundations 패키지를 import하지 않고 vocabulary만 다시 구현한다"고 선을 그어 두고 있어서, evaluator를 로컬 모듈로 다시 두되 control ID와 recommendation 문구는 그대로 맞췄다.

CLI:

```bash
$ sed -n '1,260p' study/90-capstone-collab-saas-security-review/README.md
$ sed -n '1,260p' study/90-capstone-collab-saas-security-review/docs/concepts/consolidated-remediation-workflow.md
$ sed -n '1,260p' study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/crypto.py
```

검증 신호:

- README와 concept 문서는 capstone이 product simulation이 아니라 review artifact pipeline이라고 못 박는다.
- 로컬 evaluator들은 `CRYPTO-*`, `AUTH-*`, `OWASP-*`, dependency `P1~P4`를 foundations와 같은 vocabulary로 유지한다.

핵심 코드:

```python
if controls["message_auth"] != "hmac-sha256":
    findings.append(_finding("CRYPTO-001", f"message_auth={controls['message_auth']}"))

if not controls["constant_time_compare"]:
    findings.append(_finding("CRYPTO-002", "constant_time_compare=false"))
```

왜 이 코드가 중요했는가:

capstone의 crypto review는 "새 evaluator"이면서도 foundations `01`과 같은 질문을 그대로 던진다. 그래서 `message_auth=plain-sha256`가 그대로 `CRYPTO-001`로 이어지고, timing-safe compare 누락도 별도 finding으로 남는다.

auth/backend 쪽도 같은 원리를 따른다.

```python
if flow.get("oauth_enabled") and not controls["state_required"]:
    findings.append(_finding("AUTH-001", "oauth_enabled=true인데 state_required=false"))

if surface.get("object_lookup") and not controls["ownership_scope_enforced"]:
    findings.append(_finding("OWASP-002", f"route={surface['route']}에서 ownership_scope_enforced 없이 object lookup을 수행합니다"))
```

`AUTH-001`과 `OWASP-002`가 같은 ID와 evidence shape를 유지하니, capstone 결과를 읽는 사람은 "새 개념"을 배우지 않고도 category를 넘나들 수 있다. 재사용은 import가 아니라 vocabulary stability에서 이뤄진 셈이다.

새로 배운 것:

- 통합 프로젝트에서 가장 위험한 건 로직 중복보다 vocabulary drift였다.
- 같은 finding을 다른 문장으로 다시 쓰는 순간, remediation board에서 category를 비교하기 어려워진다.

다음:

- 이제 이 local evaluator들을 review bundle 하나에 실제로 합쳐 봐야 했다.

### Session 2

- 당시 목표: `review_bundle.json` 하나를 읽어 crypto, auth, backend, dependency 결과를 같은 JSON으로 합친다.
- 변경 단위: `python/src/collab_saas_security_review/review.py`의 `build_review`, `problem/data/review_bundle.json`, `python/tests/test_review.py`
- 처음 가설: category별 CLI를 순서대로 실행한 결과를 나중에 합치면 될 줄 알았다.
- 실제 진행: 출력 형식이 흔들리지 않게 하려면 조합도 하나의 함수에서 끝나야 해서 `build_review()`가 summary와 category finding을 모두 직접 만드는 구조로 바꿨다.

CLI:

```bash
$ sed -n '1,320p' study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json
$ PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
    .venv/bin/python -m collab_saas_security_review.cli review \
    study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json
```

검증 신호:

- `review_bundle.json`은 `workspace-api`, `workspace_session_crypto_gap`, `workspace_auth_hardening_gap`, `workspace_export_gateway_gap`, dependency bundle을 한 파일에 넣는다.
- 실제 review CLI 결과는 `crypto_findings: 4`, `auth_findings: 8`, `backend_findings: 5`, `dependency_items: 4`, `remediation_items: 21`로 닫힌다.

핵심 코드:

```python
def build_review(bundle: dict[str, Any]) -> dict[str, Any]:
    crypto_review = bundle["crypto_review"]
    crypto_findings = [
        {
            **finding,
            "source": crypto_review["name"],
        }
        for finding in evaluate_crypto_review(crypto_review)
    ]

    auth_findings = [
        {
            **finding,
            "source": scenario["name"],
        }
        for scenario in bundle["auth_scenarios"]
        for finding in evaluate_scenario(scenario)
    ]
```

왜 이 코드가 중요했는가:

각 category finding에 `source`를 붙이는 순간, capstone은 단순 count 집계가 아니라 "어떤 입력이 어떤 finding을 낳았는지"까지 추적 가능한 review가 된다. remediation board에서 `source_refs`를 만들 수 있는 것도 이 source tagging 덕분이다.

summary도 여기서 같이 굳어진다.

```python
    return {
        "service": bundle["service"],
        "summary": {
            "crypto_findings": len(crypto_findings),
            "auth_findings": len(auth_findings),
            "backend_findings": len(backend_findings),
            "dependency_items": len(dependency_items),
            "remediation_items": len(remediation_board),
        },
```

service profile과 category counts가 같은 함수에서 나와야 review JSON 전체가 하나의 계약으로 유지된다. 이 구조 덕분에 secure baseline bundle이 빈 remediation board를 내는지도 같은 코드 경로에서 검증할 수 있다.

새로 배운 것:

- 통합 review에서 중요한 건 입력을 더 많이 받는 일이 아니라, category별 결과 shape를 얼마나 덜 흔들리게 유지하느냐였다.
- secure baseline bundle을 같이 두니 capstone도 false positive를 감시하는 regression suite가 됐다.

다음:

- 이제 남은 질문은 이 consolidated review를 사람이 바로 읽을 수 있는 우선순위 보드와 artifact 세트로 어떻게 바꿀 것인가였다.
