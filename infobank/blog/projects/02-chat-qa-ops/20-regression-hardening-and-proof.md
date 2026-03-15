# regression hardening과 proof

이 프로젝트의 `v2`를 읽을 때 가장 조심해야 할 부분은 "proof artifact가 말하는 역사"와 "현재 snapshot에서 지금 다시 돌린 결과"를 같은 것으로 취급하지 않는 것이다. 둘 다 중요하지만, 뜻이 다르다. historical artifact는 실제 개선 스토리를 보여 주고, current rerun은 지금 남아 있는 재현 가능성과 seam을 보여 준다.

## dashboard와 CLI는 같은 evaluation row를 다시 읽어 compare를 만든다

`dashboard.py`의 `/dashboard/version-compare`는 stored evaluation rows를 `run_label`과 `dataset`으로 다시 모아 baseline/candidate를 비교한다.

```python
result = VersionCompareResult(
    baseline=baseline,
    candidate=candidate,
    dataset=dataset or "all",
    baseline_avg=_avg(baseline_rows),
    candidate_avg=_avg(candidate_rows),
    ...
    delta=round(_avg(candidate_rows) - _avg(baseline_rows), 2),
)
```

이 구조가 중요한 이유는 compare가 별도 모델이 아니라는 점이다. 이미 evaluation pipeline이 저장한 `run_label`, `assertion_result`, `failure_types`, `total_score`를 다시 읽어 proof를 만든다. CLI의 `compare`도 같은 테이블을 출력할 뿐이다.

즉 regression proof는 새로운 계산기보다 lineage discipline의 산물이다.

## historical proof artifact는 실제 improvement story를 보존한다

`docs/demo/proof-artifacts/improvement-report.json`과 `cli-compare.txt`는 이렇게 말한다.

- `avg_score 84.06 -> 87.76`
- `critical_count 2 -> 0`
- `pass_count 16 -> 19`
- `fail_count 14 -> 11`

이 수치가 중요한 이유는 `v2`가 무엇을 개선했다고 주장하는지 가장 짧게 보여 주기 때문이다. README도 이를 `retrieval-v2 alias/category/risk rerank + retrieval-conditioned answer composer`의 결과로 설명한다. 즉 historical proof는 "baseline v1 code + retrieval-v1"과 "candidate v2 code + retrieval-v2"를 비교한 기록이다.

## 하지만 현재 snapshot 로컬 재실행은 같은 uplift를 다시 만들지 못한다

2026-03-14에 현재 snapshot에서 직접 다시 한 일은 다음과 같았다.

```bash
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make init-db
PATH="$HOME/.local/bin:$PATH" UV_PYTHON=python3.12 make seed-demo
PATH="$HOME/.local/bin:$PATH" QUALBOT_EVAL_MODE=heuristic QUALBOT_RETRIEVAL_BACKEND=keyword \
  UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run python -m cli.main evaluate --golden-set --run-label v1.0 --retrieval-version retrieval-v1
PATH="$HOME/.local/bin:$PATH" QUALBOT_EVAL_MODE=heuristic QUALBOT_RETRIEVAL_BACKEND=keyword \
  UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run python -m cli.main evaluate --golden-set --run-label v1.1 --retrieval-version retrieval-v2
PATH="$HOME/.local/bin:$PATH" QUALBOT_EVAL_MODE=heuristic QUALBOT_RETRIEVAL_BACKEND=keyword \
  UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run python -m cli.main compare v1.0 v1.1
```

현재 결과는 이렇게 나왔다.

- baseline: `87.76`, critical `0`, pass `19`, fail `11`
- candidate: `87.76`, critical `0`, pass `19`, fail `11`
- delta: `0.0`

이건 문서에서 숨길 게 아니라, 오히려 현재 snapshot의 진실이다. 이유도 추론 가능하다. 지금 남아 있는 `v2-submission-polish` 하나만으로는 historical baseline `v1` 코드 경로를 다시 실행하는 게 아니라, 같은 snapshot에 run label만 다르게 붙여 evaluation row를 만드는 셈이기 때문이다. 즉 improvement artifact는 archived proof이고, 현재 로컬 compare는 same-snapshot rerun이다.

그래서 현재 rerun의 의미를 과장하면 안 된다. 이 rerun은 "예전 개선 폭을 그대로 다시 만들었다"는 증거가 아니라, dashboard/CLI가 기대는 stored-row lineage와 compare surface가 지금도 깨지지 않았다는 non-regression evidence다. 이 구분이 있어야 historical proof와 current reproducibility를 같은 문장으로 섞지 않게 된다.

## 현재 proof surface에서 드러난 작은 seam도 남긴다

`Makefile`의 `compare` 타깃은 현재 CLI 시그니처와 맞지 않는다.

```make
compare:
	$(UV_RUN) python -m cli.main compare --baseline v1.0 --candidate v1.1
```

하지만 실제 CLI는 positional args를 받는다.

```python
@app.command("compare")
def compare(baseline: str, candidate: str, dataset: str = typer.Option("golden-set", "--dataset")) -> None:
```

그래서 `make compare`는 현재 `No such option: --baseline`으로 실패하고, 직접 `python -m cli.main compare v1.0 v1.1`로 호출해야 했다. 이런 종류의 seam은 문서에서 지우는 대신 현재 상태로 남겨 두는 편이 훨씬 낫다.

## 이번 단계의 추가 검증 신호

- `make smoke-postgres`: `PostgreSQL smoke verification passed`
- `report --format table`: 현재 top rows가 비어 있고 `Golden assertion mismatches: none`

즉 persistence path는 살아 있지만, historical improvement numbers 자체는 docs/proof-artifacts에 의존하고, current snapshot rerun은 별도 의미를 가진다.

이 단계의 결론은 단순하다. `Chat QA Ops`의 proof는 강하지만, 그 proof를 읽을 때는 historical artifact와 current rerun을 구분해야 한다. 이 구분이 있어야 다음 단계 `v3` self-hosted review ops도 과장 없이 읽을 수 있다.
