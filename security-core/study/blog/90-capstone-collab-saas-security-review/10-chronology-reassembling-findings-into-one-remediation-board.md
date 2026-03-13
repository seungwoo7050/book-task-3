# foundations vocabulary를 한 remediation board로 다시 조립하기까지

capstone의 질문은 앞선 네 프로젝트보다 훨씬 운영 쪽에 가깝다. 이제는 hash와 MAC을 구분하거나, auth control을 finding으로 바꾸거나, route defense나 dependency triage를 각각 설명하는 것만으로는 부족하다. 실제 review에서는 결국 “무엇을 먼저 고칠까”를 한 queue로 말해야 한다. 그래서 이 프로젝트는 `JSON bundle -> consolidated review -> remediation board -> artifact/report` 흐름을 만들고, foundations에서 만든 vocabulary를 하나의 우선순위 언어로 다시 정렬한다.

## 구현 순서 요약

- `crypto.py`, `auth.py`, `backend.py`, `dependency.py`에서 foundations vocabulary를 capstone bundle 안에서 다시 계산하는 evaluator를 만들었다.
- `review.py`에서 category별 finding을 합치고, severity를 `P1`~`P3`로 정규화해 remediation board를 정렬했다.
- `write_artifacts()`와 `cli.py`에서 service profile, category artifact, remediation board, markdown report를 실제 파일 세트로 만들었다.

## Session 1

capstone이라고 해서 바로 `review.py`부터 시작하지 않았다. 먼저 category evaluator를 다시 세우는 편이 맞았다. 통합 review의 설득력은 “큰 JSON을 찍었다”가 아니라, 각 category가 여전히 독립적으로 계산된다는 사실에서 나오기 때문이다.

여기서 특히 의미 있었던 선택은 foundations 패키지를 직접 import하지 않았다는 점이었다. 대신 vocabulary를 다시 구현했다. 예를 들면 crypto는 이렇게 시작한다.

```python
def evaluate_crypto_review(review: dict[str, Any]) -> list[dict[str, str]]:
    controls = review["controls"]
    findings: list[dict[str, str]] = []

    if controls["message_auth"] != "hmac-sha256":
        findings.append(_finding("CRYPTO-001", f"message_auth={controls['message_auth']}"))

    if not controls["constant_time_compare"]:
        findings.append(_finding("CRYPTO-002", "constant_time_compare=false"))
```

auth와 backend, dependency도 같은 방식으로 각자 vocabulary를 다시 계산한다. 이 선택은 겉보기에는 중복처럼 보이지만, capstone이 “패키지 재사용”보다 “review vocabulary 재사용”에 집중한다는 점을 분명히 해 준다. 같은 control ID와 priority 언어만 유지되면, 통합 review는 foundations 구현체를 직접 부르지 않아도 충분히 읽힌다.

이 단계에서 다시 돌린 검증은 capstone 테스트 전체였다.

```bash
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m pytest study/90-capstone-collab-saas-security-review/python/tests
```

검증 신호:

- `7 passed in 0.05s`
- category evaluator, review 조합, artifact writer, CLI output shape가 모두 함께 통과했다.

여기서 새로 분명해진 개념은 통합이 import graph에서 시작되지 않는다는 점이었다. 통합은 vocabulary alignment에서 시작된다. crypto는 `CRYPTO-*`, auth는 `AUTH-*`, backend는 `OWASP-*`, dependency는 `P1`~`P4`를 유지한 채 한 bundle 안에서 다시 계산되기만 하면 된다.

## Session 2

category 결과가 생기자 그다음 질문은 아주 현실적으로 바뀐다. 이걸 어떻게 한 queue로 읽을 것인가. 그 중심이 `review.py::_build_remediation_board()`였다.

```python
def _normalize_priority(severity: str) -> str:
    mapping = {
        "high": "P1",
        "medium": "P2",
        "low": "P3",
    }
    return mapping[severity]
```

이 정규화가 먼저 필요한 이유는 dependency만 이미 `P1`~`P4` priority를 갖고 있고, crypto/auth/backend는 `high`와 `medium` severity만 갖고 있기 때문이다. 같은 board 위에 올리려면 먼저 언어를 맞춰야 했다.

실제 board 조합은 이렇게 진행된다.

```python
board.sort(key=lambda item: (PRIORITY_ORDER[item["priority"]], CATEGORY_ORDER[item["category"]]))
```

코드는 짧지만, capstone 전체의 판단 전환점은 여기 있었다. `P1 -> P4`로 먼저 정렬하고, 같은 priority 안에서는 `crypto -> auth -> backend -> dependency` 순서를 유지한다. 이 규칙이 없으면 “토큰 저장 문제와 openssl CVE 중 무엇을 먼저 고칠까” 같은 질문이 다시 ad hoc하게 흐른다. 정렬 규칙을 고정한 순간, 통합 review는 예쁜 합본이 아니라 실제 remediation queue가 된다.

이 단계의 CLI는 `review`였다.

```bash
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli review \
  study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json
```

출력에서 남겨 둘 검증 신호는 숫자와 순서였다.

- `service.name`: `workspace-api`
- `summary.crypto_findings`: `4`
- `summary.auth_findings`: `8`
- `summary.backend_findings`: `5`
- `summary.dependency_items`: `4`
- `summary.remediation_items`: `21`
- `remediation_board[0].id`: `crypto:CRYPTO-001:workspace_session_crypto_gap`
- `remediation_board[-1].id`: `dependency:CVE-2026-1003:pytest`

여기서 새로 이해한 것은 “finding을 더 많이 모으는 것”과 “무엇을 먼저 고칠지 정렬하는 것”이 전혀 다른 일이라는 점이었다. capstone은 개수를 세는 프로젝트가 아니라, 우선순위 언어를 통일하는 프로젝트였다.

## Session 3

consolidated review JSON이 만들어졌다고 곧바로 운영 surface가 생기지는 않았다. 한 JSON 안에 모든 걸 넣어 두면 기계는 편하지만 사람은 오히려 읽기 어렵다. 그래서 `write_artifacts()`가 들어왔다.

```python
payloads: dict[str, Any] = {
    "01-service-profile.json": {
        "title": bundle["title"],
        "service": review["service"],
        "summary": review["summary"],
    },
    "02-crypto-findings.json": review["crypto_findings"],
    "03-auth-findings.json": review["auth_findings"],
    "04-backend-findings.json": review["backend_findings"],
    "05-dependency-items.json": review["dependency_items"],
    "06-remediation-board.json": review["remediation_board"],
}
```

이 구조가 중요했던 이유는 단순한 파일 분할이 아니라 역할 분리였기 때문이다. service profile은 리뷰어와 리더가 먼저 보고, category findings는 담당자가 세부 원인을 확인하며, remediation board는 실제 작업 queue가 된다. 사람 읽기용 markdown report도 따로 생성한다.

```python
(output_dir / "07-report.md").write_text(render_markdown_report(review))
```

`render_markdown_report()`는 화려한 렌더러는 아니지만, capstone이 사람 읽는 문서까지 책임진다는 점을 분명히 한다. foundations 프로젝트들이 모두 CLI와 pytest로 닫혔다면, capstone은 거기에 artifact 세트까지 추가해 “회의에 붙여 넣을 수 있는 결과물”로 마감한다.

실제 artifact 생성은 demo로 확인했다.

```bash
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli demo \
  study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json
```

이때 남긴 검증 신호는 단순 메시지가 아니라 생성된 파일 목록이었다.

- `demo 산출물을 .artifacts/capstone/demo에 기록했습니다`
- `01-service-profile.json`
- `02-crypto-findings.json`
- `03-auth-findings.json`
- `04-backend-findings.json`
- `05-dependency-items.json`
- `06-remediation-board.json`
- `07-report.md`

여기서 배운 것은 artifact 분리가 중복이 아니라 review surface 설계라는 점이었다. 하나의 JSON은 개발자에게는 편하지만, 운영자와 리뷰어, 담당자에게는 각자 다른 entrypoint가 필요하다. 이 capstone이 통합 프로젝트로 읽히는 이유도 바로 그 표면 분리에 있다.

## Session 4

마지막으로 이 capstone이 과장된 데모로 끝나지 않으려면 baseline이 필요했다. 그래서 `test_review.py`와 `test_cli.py`가 secure baseline, remediation board ordering, artifact file set을 함께 고정한다.

가장 중요한 테스트는 빈 review였다.

```python
def test_secure_baseline_bundle_emits_empty_review() -> None:
    review = build_review_from_path(DATA_DIR / "secure_baseline_bundle.json")
    assert review["summary"] == {
        "crypto_findings": 0,
        "auth_findings": 0,
        "backend_findings": 0,
        "dependency_items": 0,
        "remediation_items": 0,
    }
```

이 테스트가 없었으면 capstone은 취약한 bundle을 멋지게 조합하는 데모로만 남았을 것이다. 그런데 baseline이 0건으로 고정되자, remediation board의 의미가 훨씬 정확해졌다. review는 무조건 뭔가를 만들어 내는 기계가 아니라, 실제로 비어 있을 수도 있는 queue가 된다.

CLI 테스트도 같은 방향이었다.

```python
assert sorted(path.name for path in tmp_path.iterdir()) == [
    "01-service-profile.json",
    "02-crypto-findings.json",
    "03-auth-findings.json",
    "04-backend-findings.json",
    "05-dependency-items.json",
    "06-remediation-board.json",
    "07-report.md",
]
```

이 file set이 고정되면서 capstone은 단순 JSON generator가 아니라 artifact contract를 가진 review pipeline이 된다. category별 근거와 최종 queue, 사람 읽는 보고서가 같은 contract 안에서 묶인다는 뜻이기도 하다.

## 다음

이 capstone이 만든 것은 보안 기능 모음이 아니라 review queue를 설명하는 최소 운영 문서다. 앞선 네 프로젝트에서 primitive, control, route defense, triage action으로 갈라 놓은 vocabulary가 마지막에 여기서 다시 만나면서, `security-core` 전체가 작은 실행 가능한 보안 판단 아카이브로 닫힌다.
