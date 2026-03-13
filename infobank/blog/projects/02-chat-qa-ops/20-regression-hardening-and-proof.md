# regression hardening과 proof

앞 글에서 평가 파이프라인이 어떻게 세워졌는지 봤다면, 이번에는 그 파이프라인이 어떻게 "증빙"이 되었는지 본다. 여기서 따라갈 질문은 하나다. 상담 품질이 좋아졌다는 말을, 감이 아니라 같은 golden set 위의 숫자로 어떻게 고정했을까?

`v2-submission-polish`의 중심은 retrieval을 조금 더 똑똑하게 만든 것만이 아니다. baseline과 candidate의 차이를 같은 데이터셋 위에서 비교하고, 그 결과를 dashboard와 runbook, proof artifact까지 연결했다는 점이 핵심이다.

이 구간의 요점을 가장 짧게 보여 주는 자료가 `docs/demo/proof-artifacts/improvement-report.json`이다.

```json
{
  "baseline": { "run_label": "v1.0", "avg_score": 84.06, "critical_count": 2, "pass_count": 16, "fail_count": 14 },
  "candidate": { "run_label": "v1.1", "avg_score": 87.76, "critical_count": 0, "pass_count": 19, "fail_count": 11 }
}
```

이 숫자가 중요한 이유는 단순히 점수가 올랐기 때문이 아니다. 같은 `run_label`, 같은 `dataset`, 같은 assertion 구조를 유지한 채 비교했기 때문에, 이 변화가 실제 회귀 개선으로 읽힌다.

그 비교를 코드에서 받아 주는 곳이 `python/backend/src/api/routes/dashboard.py`의 version compare 경로다.

아래 블록은 compare가 별도 계산기를 쓰는 것이 아니라, 이미 쌓인 evaluation row를 다시 읽어 proof를 만드는 구조라는 점을 보여 준다.

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

좋은 점은 dashboard가 화면용 숫자를 따로 들고 있지 않다는 것이다. `run_label`, `dataset`, `assertion_result`, `failure_types`가 이미 evaluation row에 남아 있으니, compare는 그 저장 구조를 다시 읽으면 된다. 그래서 `docs/demo/phase1-vs-phase2-diff-matrix.md`가 말하는 "UI 차이가 작아도 내부 지표 차이로 Phase2를 증명한다"는 원칙이 실제 코드에서도 그대로 유지된다.

CLI 증거도 남아 있다. proof artifact로 저장된 `cli-compare.txt`는 바로 이렇게 요약한다.

```text
avg_score: 84.06 -> 87.76 (delta 3.7)
critical_count: 2 -> 0 (delta -2)
pass_count: 16 -> 19 (delta 3)
fail_count: 14 -> 11 (delta -3)
```

이 출력이 증명하는 것은 세 가지다. 평균 점수가 올랐고, critical 수가 줄었고, assertion pass가 늘었다. 즉 "좋아졌다"는 말이 하나의 감상이 아니라 여러 관점의 숫자로 고정된다.

`cli-report.txt`는 더 세밀한 최신 evaluation row를 보여 주고, runbook은 이 compare 수치를 실제 발표 흐름 안에 배치한다. 다시 말해 이 프로젝트의 proof는 JSON 한 장으로 끝나지 않는다. CLI, API, 대시보드, 발표 문서가 같은 개선 수치를 반복해서 가리킨다.

운영성 근거도 여기에 붙는다. `UV_PYTHON=python3.12 make smoke-postgres`를 실제로 돌리면 아래처럼 데이터베이스 경로가 살아 있음을 다시 확인할 수 있다.

```text
PostgreSQL smoke verification passed
```

이 메시지가 중요한 이유는 regression proof가 메모리 안에서만 도는 데모가 아니라, 실제 persistence와 함께 재현 가능한 흐름이라는 사실을 보여 주기 때문이다. `docs/verification-matrix.md`가 `gate-all`과 별도로 `smoke-postgres`를 적어 둔 이유도 여기 있다.

결국 `v2`에서 완성된 것은 retrieval 개선 하나가 아니다. 더 중요한 건 operator가 "candidate가 좋아졌는가"를 감으로 말하지 않아도 되는 proof chain이다. run label, dataset, assertion, failure taxonomy, dashboard compare, smoke path가 같은 구조 안에 붙으면서 이 트랙은 진짜 QA Ops처럼 읽히기 시작한다.

다음 글에서는 이 proof chain을 그대로 들고 가서 self-hosted OSS surface로 옮긴 `v3`를 본다. baseline과 candidate compare가 이번에는 dataset upload, KB bundle, evaluation job, selected-job review UI 안으로 들어간다.
