# 10 Cloud Security Control Plane: 아홉 개의 판단 로직을 control plane으로 묶기

앞선 아홉 개 프로젝트의 판단 로직을 scan, ingestion, exception, remediation, report 흐름으로 묶어 내는 통합 capstone이다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "통합 capstone에서 먼저 세워야 할 경계는 API인가, scanner 로직인가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. FastAPI 앱이 scan/ingest/findings/exceptions/remediations/report API를 하나의 session factory 위에 올렸다.
2. worker 계층이 pending scan/remediation 요청을 처리하고 findings와 audit를 저장하게 했다.
3. demo capture가 end-to-end 시나리오를 실행해 report와 demo asset을 남기고, PostgreSQL이 없을 때는 SQLite fallback으로도 재현되게 했다.

## Phase 1. API 표면과 상태 저장소 경계를 먼저 세웠다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `API 표면과 상태 저장소 경계를 먼저 세웠다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 여러 보안 입력이 한 서비스 안으로 들어오는 기본 통로를 만든다.
- 변경 단위: `python/src/cloud_security_control_plane/app.py`의 `create_app`, `python/src/cloud_security_control_plane/db.py`의 session factory
- 처음 가설: 통합 프로젝트일수록 새 로직을 많이 쓰기보다, 기존 스캐너를 얇게 감싸는 API/DB 경계를 먼저 세우는 편이 안전하다.
- 실제 진행: `create_app`은 database URL과 lake 디렉터리를 app state에 저장하고, `session_factory`와 `metrics`를 함께 묶었다. 동시에 `/v1/scans`, `/v1/ingestions/*`, `/v1/findings`, `/v1/exceptions`, `/v1/remediations/*`, `/v1/reports/latest` 라우트를 한곳에 올려 control plane의 외형을 만들었다.

CLI:

```bash
$ PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json
```

검증 신호:
- CLI가 `CSPM-001`, `CSPM-002`, `CSPM-003` 세 finding을 JSON으로 출력했다.
- `db.default_database_url()`은 기본적으로 SQLite fallback 경로를 가리키고, `normalize_database_url()`은 postgres URL을 psycopg 형태로 맞춘다.

핵심 코드:

```python
def create_app(database_url: str | None = None, lake_dir: str | None = None) -> FastAPI:
    app = FastAPI(title="Cloud Security Control Plane")
    app.state.database_url = db.normalize_database_url(database_url or db.default_database_url())
    app.state.lake_dir = Path(lake_dir or os.environ.get("CONTROL_PLANE_LAKE_DIR", ".artifacts/capstone/lake"))
    app.state.metrics = Metrics()
    app.state.session_factory = db.make_session_factory(app.state.database_url)

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/metrics", response_class=PlainTextResponse)
    def metrics() -> str:
        return app.state.metrics.render()

    @app.post("/v1/scans")
    def create_scan(payload: ScanRequest) -> dict[str, str]:
        with app.state.session_factory() as session:
            job = db.create_scan_job(session, payload.source, payload.path)
            session.commit()
        app.state.metrics.inc("scan_jobs_created_total")
        return {"id": job.id, "status": job.status}
```

왜 이 코드가 중요했는가: 이 부분이 있어야 capstone이 “모듈 모음”이 아니라 서비스가 된다. API 표면과 state 경계가 먼저 생겨야 그 위에 workers와 reports를 얹을 수 있다.

새로 배운 것: 통합 레이어의 핵심은 비즈니스 로직을 다시 쓰는 게 아니라, 기존 판단 로직이 같은 저장소와 같은 인터페이스를 공유하게 만드는 것이다.

다음: 이제 pending scan/remediation 요청을 실제 처리하는 worker 계층을 붙여야 했다.

## Phase 2. worker가 scanner와 저장소를 연결했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `worker가 scanner와 저장소를 연결했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: scan 요청과 remediation 요청이 상태 전이를 거쳐 결과를 저장하게 만든다.
- 변경 단위: `python/src/cloud_security_control_plane/workers.py`, `python/src/cloud_security_control_plane/db.py`의 `save_findings`, `create_scan_job`, `list_findings`
- 처음 가설: 요청을 받는 API와 실제 처리를 섞으면 capstone이 금방 커진다. worker로 분리하면 pending/completed 상태를 설명하기 쉬워진다.
- 실제 진행: `process_pending_scans`는 source에 따라 Terraform/IAM scanner를 호출하고 finding 저장과 metrics 증가를 맡았다. `ingest_cloudtrail_and_save`, `ingest_k8s_and_save`는 각각 lake 적재나 manifest scanning을 수행한 뒤 finding과 audit event를 저장하게 했다. DB 레이어는 findings, exceptions, remediation requests/plans, scan jobs를 같은 SQLAlchemy 모델로 관리한다.

CLI:

```bash
$ make test-capstone
```

검증 신호:
- `make test-capstone`이 `1 passed in 0.64s`로 end-to-end 테스트를 통과했다.
- 테스트는 scan request 두 건 처리 후 `processed_jobs == 2`, findings 6건 이상, suppression 반영, remediation dry-run 생성까지 확인한다.

핵심 코드:

```python
def process_pending_scans(database_url: str, lake_dir: Path, metrics: Metrics) -> int:
    session_factory = db.make_session_factory(database_url)
    processed = 0
    with session_factory() as session:
        jobs = db.pending_scan_jobs(session)
        for job in jobs:
            if job.source == "terraform-plan":
                findings = scan_terraform_plan(Path(job.path))
            elif job.source == "iam-policy":
                findings = scan_iam_policy(Path(job.path))
            else:
                findings = []
            db.save_findings(session, findings)
            db.complete_scan_job(session, job, len(findings))
            metrics.inc("scan_jobs_processed_total")
            metrics.inc("findings_created_total", len(findings))
            processed += 1
        session.commit()
    return processed


def ingest_cloudtrail_and_save(database_url: str, lake_dir: Path, path: Path, metrics: Metrics) -> int:
    session_factory = db.make_session_factory(database_url)
    _, findings = ingest_cloudtrail(path, lake_dir)
    with session_factory() as session:
        db.save_findings(session, findings)
        db.record_audit_event(session, "cloudtrail.ingested", str(path), {"finding_count": str(len(findings))})
        session.commit()
    metrics.inc("cloudtrail_ingestions_total")
    metrics.inc("findings_created_total", len(findings))
    return len(findings)
```

왜 이 코드가 중요했는가: worker 계층이 들어오면서 control plane은 “즉시 계산기”가 아니라 상태 기반 서비스가 됐다. 요청을 저장하고 나중에 처리하는 흐름이 생겼기 때문이다.

새로 배운 것: control plane에서 중요한 분리는 sync API와 async-like worker의 역할 분담이다. 그래야 pending/completed, metrics, audit가 자연스럽게 붙는다.

다음: 이제 remediation과 report를 붙여 전체 운영 흐름을 끝까지 닫아야 했다.

## Phase 3. remediation과 report로 운영 흐름을 닫았다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `remediation과 report로 운영 흐름을 닫았다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: finding이 예외와 조치안과 보고서까지 이어지는 마지막 경로를 만든다.
- 변경 단위: `python/src/cloud_security_control_plane/reporting.py`, `python/src/cloud_security_control_plane/remediation.py`, `/v1/remediations/*`, `/v1/reports/latest`
- 처음 가설: capstone이 포트폴리오처럼 보이려면 탐지에서 끝나지 않고, suppressed finding과 dry-run plan이 같은 보고서에 보여야 한다.
- 실제 진행: remediation builder는 CSPM control에 따라 auto/manual mode를 선택하고, report generator는 findings, exceptions, remediation plans를 한 Markdown 문서로 합쳤다. DB 레이어는 active exception scope를 읽어 finding status를 `suppressed`로 바꿔 report에 반영한다.

CLI:

```bash
$ make demo-capstone
```

검증 신호:
- `make demo-capstone` 실행이 `demo assets written to .../.artifacts/capstone/demo`로 끝났다.
- 생성된 demo asset에서 scan worker는 `processed_jobs: 2`, CloudTrail은 `finding_count: 2`, k8s ingest는 `finding_count: 3`을 기록했다.
- 최종 report에는 suppressed `CSPM-001`, open `CSPM-002`, `IAM-*`, `LAKE-*`, `K8S-*` findings와 예외 1건, remediation plan 1건이 함께 들어갔다.

핵심 코드:

```python
def generate_markdown_report(
    findings: list[Finding],
    exceptions: list[ExceptionRecord],
    remediations: list[RemediationPlan],
) -> str:
    lines = [
        "# Cloud Security Control Plane Report",
        "",
        "## Findings",
    ]
    if findings:
        for finding in findings:
            lines.append(
                f"- `{finding.control_id}` `{finding.severity}` `{finding.status}` `{finding.resource_id}`: {finding.title}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Exceptions"])
    if exceptions:
        for record in exceptions:
            lines.append(
                f"- `{record.scope_id}` `{record.status}` expires `{record.expires_at.isoformat()}` reason: {record.reason}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Remediation Plans"])
    if remediations:
        for plan in remediations:
            lines.append(f"- `{plan.finding_id}` `{plan.mode}` `{plan.status}`: {plan.summary}")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"
```

왜 이 코드가 중요했는가: 이 함수가 들어오면서 capstone은 단순 CRUD API가 아니라 “탐지 -> 예외 -> 조치안 -> 보고서”를 한 화면에서 설명하는 control plane이 됐다.

새로 배운 것: 보안 플랫폼의 가치는 finding 개수보다 흐름을 연결하는 데 있다. suppressed status와 remediation mode가 같은 report에 들어갈 때 비로소 운영 맥락이 보인다.

다음: 마지막으로 이 모든 흐름을 한 번의 demo capture로 남겨야 했다.

## Phase 4. demo capture와 fallback으로 재현성을 마감했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `demo capture와 fallback으로 재현성을 마감했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 사람이 수동으로 API를 두드리지 않아도 end-to-end 시나리오를 다시 만들 수 있게 한다.
- 변경 단위: `python/src/cloud_security_control_plane/demo_capture.py`, `docs/demo-walkthrough.md`, `.artifacts/capstone/demo/*`
- 처음 가설: 캡스톤은 설명할 게 많아서, 문서만으로는 재현성이 약하다. demo asset을 파일로 남겨야 결과를 나중에 다시 확인할 수 있다.
- 실제 진행: `demo_capture.py`는 scan request, worker run, cloudtrail/k8s ingestion, exception 생성, remediation dry-run, report export를 순서대로 실행한 뒤 결과를 `01`~`08` 파일로 남겼다. Makefile은 Docker daemon이 있으면 PostgreSQL 경로를, 없으면 SQLite 경로를 택해 같은 시나리오를 재현한다.

CLI:

```bash
$ make demo-capstone
$ PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json
```

검증 신호:
- 실제 실행에서는 Docker 경로로 올라가 `postgres healthy` 뒤 demo asset이 생성됐다.
- 문서 `docs/demo-walkthrough.md`와 실제 demo JSON이 같은 숫자들(`processed_jobs 2`, `cloudtrail 2`, `k8s 3`)을 가리킨다.

핵심 코드:

```python
    scan_responses: list[dict[str, object]] = []
    scan_responses.append(client.post("/v1/scans", json={"source": "terraform-plan", "path": str(data_dir / "insecure_plan.json")}).json())
    scan_responses.append(client.post("/v1/scans", json={"source": "iam-policy", "path": str(data_dir / "broad_admin_policy.json")}).json())
    worker_response = client.post("/v1/workers/scans/run").json()
    cloudtrail_response = client.post("/v1/ingestions/cloudtrail", json={"path": str(data_dir / "cloudtrail_suspicious.json")}).json()
    k8s_response = client.post("/v1/ingestions/k8s", json={"path": str(data_dir / "insecure_k8s.yaml")}).json()
    findings_response = client.get("/v1/findings").json()

    findings = findings_response["findings"]
    first_finding_id = findings[0]["id"]
    second_finding_id = findings[1]["id"]

    exception_response = client.post(
        "/v1/exceptions",
        json={
            "scope_type": "finding",
            "scope_id": first_finding_id,
            "reason": "Temporary business exception for demo",
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            "approved_by": "security.manager",
        },
    ).json()
    remediation_response = client.post(f"/v1/remediations/{second_finding_id}/dry-run").json()
    report_response = client.get("/v1/reports/latest").json()

    (asset_dir / "01-scan-requests.json").write_text(json.dumps(scan_responses, indent=2))
    (asset_dir / "02-worker-response.json").write_text(json.dumps(worker_response, indent=2))
    (asset_dir / "03-cloudtrail-response.json").write_text(json.dumps(cloudtrail_response, indent=2))
    (asset_dir / "04-k8s-response.json").write_text(json.dumps(k8s_response, indent=2))
    (asset_dir / "05-findings.json").write_text(json.dumps(findings_response, indent=2))
    (asset_dir / "06-exception.json").write_text(json.dumps(exception_response, indent=2))
    (asset_dir / "07-remediation.json").write_text(json.dumps(remediation_response, indent=2))
    (asset_dir / "08-report.md").write_text(report_response["markdown"])

    print(f"demo assets written to {asset_dir}")
```

왜 이 코드가 중요했는가: demo capture가 있기 전에는 capstone이 “잘 짠 구조”로만 남는다. 이 스크립트가 들어오면서 같은 흐름을 파일로 보여 줄 수 있는 살아 있는 프로젝트가 됐다.

새로 배운 것: 통합 프로젝트일수록 재현성은 테스트 한 줄보다 demo artifact에 더 잘 남는다. 구조와 결과를 함께 보존하기 때문이다.

다음: 이제 control plane은 로컬 학습용 capstone으로는 충분히 닫혔다. 남은 확장은 외부 큐, 실제 AWS 연동, 인증/멀티테넌시 쪽이다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 capstone의 성과는 새로운 탐지 로직을 많이 추가한 데 있지 않다. 앞선 프로젝트들의 판단을 같은 API, 같은 DB, 같은 report 흐름으로 묶어 운영 서사를 만들었다는 데 있다. 그래서 하나의 demo만 돌려도 Terraform, IAM, CloudTrail, Kubernetes, exception, remediation, reporting을 함께 설명할 수 있다.
