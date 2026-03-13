# Regression Hardening And Proof

앞 글에서 baseline evaluation loop를 만들었다면, 이 글은 그 loop가 어떻게 regression proof 시스템으로 자랐는지 따라간다. `v1`에서는 provider failure를 trace 안으로 끌어오고, `v2`에서는 retrieval-v2 실험을 compare artifact와 improvement report로 굳힌다.

구현 순서 요약:

- provider chain이 외부 모델 의존성을 단일 실패 지점이 아니라 순차 fallback과 attempt trace로 바꿨다.
- retrieval-v2는 alias/category/risk rerank와 retrieval-conditioned answer composer를 같이 넣어 안전한 답변 경로를 강화했다.
- compare proof는 "느낌상 좋아졌다"가 아니라 golden-set 기준 JSON artifact로 남겼다.

## Day 2

### Session 1

- 당시 목표: provider 하나가 흔들려도 evaluation과 answer generation이 바로 무너지지 않는 hardening 경로를 만든다.
- 변경 단위: `core/provider_chain.py`
- 처음 가설: 단일 provider + timeout 정도면 제출용 QA Ops에는 충분할 것이라고 봤다.
- 실제 진행: provider chain이 설정된 순서대로 `upstage`, `openai`, `ollama`를 시도하고, 성공/실패/latency를 `ProviderAttempt` trace로 남기게 했다.

핵심 코드는 provider loop 자체에 있다.

```py
def generate_json(self, *, system_prompt: str, user_prompt: str, model_hint: str | None = None) -> tuple[dict[str, Any], list[ProviderAttempt]]:
    attempts: list[ProviderAttempt] = []
    for provider in self.settings.provider_chain:
        payload, attempt = self._generate(
            provider,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            want_json=True,
            model_hint=model_hint,
        )
        attempts.append(attempt)
        if isinstance(payload, dict):
            return payload, attempts
    raise DependencyUnavailableError("provider", self._build_error_message(attempts, "json"))
```

그리고 실패를 그냥 삼키지 않는다.

```py
joined = ", ".join(
    f"{attempt.provider}:{attempt.error or 'unknown error'}"
    for attempt in attempts
)
return f"Provider chain failed for {mode} generation: {joined}"
```

왜 이 코드가 중요했는가:

이전에는 모델 호출 실패가 "운이 나빴다"로 끝날 수 있었다. 하지만 provider chain 이후에는 어떤 provider가 왜 실패했는지 trace에 남는다. regression은 품질 점수만이 아니라 dependency failure path까지 포함하는 일로 넓어졌다.

CLI:

```bash
$ UV_PYTHON=python3.12 make smoke-postgres
PostgreSQL smoke verification passed
```

이 smoke 출력이 중요한 이유는, hardening이 단순히 코드 추상화에 그치지 않고 PostgreSQL 기반 session, evaluation, API 기동 경로에서도 버텨야 한다는 걸 확인하기 때문이다.

새로 배운 것:

provider fallback은 선택 옵션이 아니라, 품질 평가 trace를 깨지 않기 위한 안정성 계층이었다.

## Day 3

### Session 1

- 당시 목표: retrieval 실험을 체감 향상이 아니라 golden-set compare proof로 남긴다.
- 변경 단위: `chatbot/retriever.py`, `chatbot/bot.py`, `backend/src/cli/main.py`, `docs/demo/proof-artifacts/*.json`
- 처음 가설: keyword overlap만 잘 맞춰도 제출용 QA Ops 데모는 충분히 설득될 것이라고 봤다.
- 실제 진행: query alias, category trigger, risk flag를 조합한 `retrieval-v2` plan을 만들고, 답변 composer도 분쟁/개인정보/본인확인 질문이면 해당 정책 문서를 우선 노출하게 바꿨다.

retrieval-v2의 핵심은 "검색 점수를 조금 올린다"가 아니라 질문 유형을 먼저 해석한다는 점이다.

```py
if any(term in normalized_query for term in ("분쟁", "민원", "환불 거절", "피해")):
    categories.insert(0, "policies")
    risk_flags.append("escalation")
if any(term in normalized_query for term in ("주민번호", "카드번호", "개인정보")):
    categories.insert(0, "policies")
    risk_flags.append("privacy")
if any(term in normalized_query for term in ("본인인증", "본인확인", "인증", "명의변경", "해지", "환불")):
    categories.insert(0, "procedures")
    risk_flags.append("verification")
```

answer composer도 같은 risk 방향을 따른다.

```py
add_doc(docs[0])
if any(keyword in user_message for keyword in ["분쟁", "민원", "환불 거절", "피해"]):
    add_doc(next((doc for doc in docs if doc.doc_id == "policies__escalation_policy.md"), None))
if any(keyword in user_message for keyword in ["주민번호", "카드번호", "개인정보"]):
    add_doc(next((doc for doc in docs if doc.doc_id == "policies__privacy_policy.md"), None))
if any(keyword in user_message for keyword in ["본인인증", "본인확인", "인증", "명의변경", "해지", "환불"]):
    add_doc(next((doc for doc in docs if doc.doc_id == "procedures__identity_verification.md"), None))
```

왜 이 코드가 중요했는가:

retrieval-v2는 검색 결과를 더 많이 맞히려는 기능이 아니다. 위험 질문이 들어왔을 때 어떤 정책과 절차 문서를 반드시 같이 보여 줄지 규칙을 먼저 박아 둔 retrieval layer다.

비교 증빙은 committed artifact에서 읽는다.

```bash
$ sed -n '1,120p' docs/demo/proof-artifacts/improvement-report.json
baseline avg_score: 84.06
candidate avg_score: 87.76
baseline critical_count: 2
candidate critical_count: 0

$ sed -n '1,120p' docs/demo/proof-artifacts/api-version-compare.json
delta: 3.7
pass_delta: 3
fail_delta: -3
critical_delta: -2
```

그리고 source-level compare entrypoint는 이렇게 정의돼 있다.

```py
@app.command("compare")
def compare(baseline: str, candidate: str, dataset: str = typer.Option("golden-set", "--dataset")) -> None:
```

이 대목이 중요한 이유는, 현재 Makefile은 여전히 `--baseline/--candidate` 플래그를 쓰고 있어서 live rerun path가 drift가 있기 때문이다. 그래서 여기서는 stale target을 무시하고, CLI 시그니처와 committed proof artifact JSON을 같이 근거로 사용한다.

CLI:

```bash
$ UV_PYTHON=python3.12 make gate-all
ruff check: OK
mypy: OK
MP1: 3 passed
MP2: 5 passed
MP3: 15 passed
MP4: 5 passed
MP5: 16 passed
frontend vitest: 5 passed
Integrity gate passed for target=all
```

검증 신호:

- gate-all은 여전히 green이고,
- compare artifact는 `84.06 -> 87.76`, critical `2 -> 0`, pass `16 -> 19`를 고정해 준다.

새로 배운 것:

retrieval 개선은 score delta만으로 증명되지 않는다. 어떤 risk 문서를 우선 노출했는지와 그 결과가 golden-set compare에 어떻게 찍혔는지까지 같이 남겨야 proof가 된다.

## 다음

proof artifact가 생긴 뒤에는 제출용 데모를 누가 어떻게 다시 실행할지 경계가 필요해진다. 다음 글에서는 `v3`의 `/api/evaluate/*`와 `/api/jobs`가 어떻게 self-hosted review ops 제품으로 분리되는지 본다.
