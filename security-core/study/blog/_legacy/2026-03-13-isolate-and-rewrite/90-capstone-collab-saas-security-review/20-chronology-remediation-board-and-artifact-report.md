# 20 Remediation Board And Artifact Report

이 글은 capstone 전체에서 consolidated review JSON이 실제 운영 문서처럼 읽히는 remediation board와 artifact 세트로 변하는 구간이다. 흐름은 `priority normalization -> board sort -> markdown report와 artifact writer` 순서로 따라간다.

## Day 2
### Session 1

- 당시 목표: crypto/auth/backend finding과 dependency triage item을 한 우선순위 언어로 정렬한다.
- 변경 단위: `python/src/collab_saas_security_review/review.py`의 `_normalize_priority`, `_build_remediation_board`
- 처음 가설: severity 문자열과 dependency `P1~P4`를 그대로 섞어도 정렬이 가능할 줄 알았다.
- 실제 진행: category마다 언어가 달라서 `high/medium/low`를 `P1/P2/P3`로 정규화하고, 같은 priority 안에서는 `crypto -> auth -> backend -> dependency` 순서를 따로 고정했다.

CLI:

```bash
$ sed -n '1,260p' study/90-capstone-collab-saas-security-review/docs/concepts/consolidated-remediation-workflow.md
$ sed -n '1,260p' study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/review.py
```

검증 신호:

- concept 문서는 "severity는 `P1~P3`로 정규화하고 dependency는 기존 priority를 유지한다"고 미리 못 박는다.
- review CLI 출력에서도 remediation board 첫 항목은 `crypto:CRYPTO-001:workspace_session_crypto_gap`, 마지막 항목은 `dependency:CVE-2026-1003:pytest`로 정렬된다.

핵심 코드:

```python
def _normalize_priority(severity: str) -> str:
    mapping = {
        "high": "P1",
        "medium": "P2",
        "low": "P3",
    }
    return mapping[severity]
```

왜 이 코드가 중요했는가:

이 매핑이 없으면 `AUTH-001`과 `CVE-2026-1001`을 같은 보드에서 비교할 방법이 없다. capstone의 핵심은 finding을 더 만드는 데 있지 않고, 다른 종류의 위험을 같은 우선순위 문법으로 묶는 데 있다.

정렬 규칙도 명시적으로 남긴다.

```python
board.sort(key=lambda item: (PRIORITY_ORDER[item["priority"]], CATEGORY_ORDER[item["category"]]))
```

priority만 정렬하면 category가 섞여 읽기 어려워진다. 같은 `P1` 안에서 crypto와 auth가 먼저 오고, backend와 dependency가 뒤따르도록 고정해 두니 review meeting에서 설명 순서도 안정된다.

새로 배운 것:

- remediation board는 데이터 구조이면서 동시에 발표 순서다.
- 그래서 sort 규칙은 UX 세부사항이 아니라 review 품질의 일부였다.

다음:

- 이제 이 보드를 JSON 안에만 두지 않고, 사람이 읽는 report와 artifact 7종으로 바꿔야 했다.

### Session 2

- 당시 목표: consolidated review를 서비스 요약, category JSON, remediation board, markdown report로 쪼개 쓴다.
- 변경 단위: `python/src/collab_saas_security_review/review.py`의 `render_markdown_report`, `write_artifacts`, `python/src/collab_saas_security_review/cli.py`, `docs/demo-walkthrough.md`
- 처음 가설: review CLI 출력 JSON 하나만 있으면 충분할 것 같았다.
- 실제 진행: JSON 하나는 기계엔 좋지만 사람이 훑기 어렵고, category 담당자도 필요한 부분만 보고 싶어서 artifact 7종으로 분리했다.

CLI:

```bash
$ PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
    .venv/bin/python -m pytest study/90-capstone-collab-saas-security-review/python/tests
.......                                                                  [100%]
7 passed in 0.05s
```

```bash
$ rm -rf .artifacts/capstone/demo
$ PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
    .venv/bin/python -m collab_saas_security_review.cli demo \
    study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json
demo 산출물을 .artifacts/capstone/demo에 기록했습니다
$ sed -n '1,120p' .artifacts/capstone/demo/07-report.md
```

검증 신호:

- demo walkthrough가 말한 그대로 `.artifacts/capstone/demo/` 아래 `01-service-profile.json`부터 `07-report.md`까지 7개 파일이 생성된다.
- `07-report.md`는 `서비스 요약 -> 암호 finding -> 인증 finding -> 백엔드 finding -> 의존성 큐 -> 조치 보드` 섹션 순서를 정확히 가진다.

핵심 코드:

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

왜 이 코드가 중요했는가:

artifact를 category별로 나누니 review 소비자도 자연스럽게 갈라진다. 경영진은 `01-service-profile.json`과 `06-remediation-board.json`만 봐도 되고, 각 담당자는 자기 category JSON만 보면 된다. capstone이 "통합"을 하면서도 결과를 다시 분리해 쓰는 이유가 바로 여기 있다.

report 렌더링은 그 위에 얇게 얹힌다.

```python
lines = [
    "# 서비스 요약",
    f"- 서비스 이름: `{review['service']['name']}`",
    f"- tenant model: `{review['service']['tenant_model']}`",
    f"- internet exposed: `{review['service']['internet_exposed']}`",
    ...
]
```

사람 읽기용 report를 별도로 만드는 이유는 meeting notes나 PR 설명에 그대로 붙일 수 있게 하기 위해서다. JSON이 source of truth라면, markdown report는 전달 계층이다. `write_artifacts()`가 둘을 함께 쓰니 둘 사이 드리프트도 막을 수 있다.

새로 배운 것:

- 통합 review의 마지막 산출물은 JSON이 아니라 "누가 무엇부터 고칠지 바로 읽히는 문서"였다.
- demo CLI가 실제 서비스가 아니라 artifact를 생성하게 만든 선택도 그래서 맞았다. 이 capstone의 핵심은 운영 infra가 아니라 review 전달물이다.

다음:

- 범위를 넓힌다면 외부 advisory API나 실제 queue를 붙이기보다, 지금 artifact 세트가 어떤 팀 경계에서 충분하고 어디서 부족한지부터 다시 점검해야 한다.
