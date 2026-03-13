# 20 Workers, State, And Reporting

이 문서는 capstone의 worker, 상태 저장소, suppression, remediation, report 경계를 현재 DB/worker 코드만으로 다시 읽은 기록입니다.

## Day 2
### Session 1

- 목표: finding이 어디에 저장되고, exception이 어떻게 suppression으로 반영되는지 확인한다.
- 진행: `db.py`, `workers.py`, `reporting.py`, `remediation.py`를 읽고 `test_api.py`의 후반부 assertion을 다시 대조했다.
- 이슈: 처음엔 모든 상태가 메모리 안에서만 돌 거라 생각했는데, 실제 구현은 SQLAlchemy row와 session factory를 중심으로 얇은 저장 계층을 세워 두고 있었다.
- 판단: 이 프로젝트의 핵심은 “스캐너 결과를 내는 것”보다 “그 결과를 어떤 row로 저장하고 어떤 시점에 status를 바꿀 것인가”에 있었다.

CLI:

```bash
$ sed -n '1,260p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/db.py
$ sed -n '1,240p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/workers.py
$ sed -n '1,220p' 02-capstone/10-cloud-security-control-plane/python/tests/test_api.py
```

이 시점의 핵심 코드는 approved exception을 finding status overlay로 반영하는 부분이었다.

```python
def list_findings(session: Session) -> list[Finding]:
    suppressed = active_exception_scope_ids(session)
    rows = session.scalars(select(FindingRecord).order_by(FindingRecord.detected_at)).all()
    return [
        Finding(
            ...
            status="suppressed" if row.id in suppressed else row.status,
            ...
        )
        for row in rows
    ]
```

처음엔 exception row를 따로 조회하는 것만으로 충분하다고 생각했지만, 실제로는 `list_findings()`에서 suppression을 overlay 해야 API 사용자가 별도 join 없이도 현재 상태를 바로 읽을 수 있다. 이 조각이 없으면 exception 모델과 findings 표면이 따로 놀게 된다.

### Session 2

- 진행: remediation builder와 markdown report generator를 같이 읽어 finding 이후 흐름이 어디서 마무리되는지 확인했다.
- 이슈: 처음엔 remediation이 patch 텍스트만 만드는 단계라고 생각했는데, report를 보니 exceptions와 remediations까지 함께 묶여 최종 운영 문서 역할을 하고 있었다.
- 판단: capstone에서 report는 부가 산출물이 아니라, 여러 하위 프로젝트의 결과를 한 화면으로 다시 묶는 마지막 계층이다.

CLI:

```bash
$ make demo-capstone
$ sed -n '1,200p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/remediation.py
$ sed -n '1,200p' 02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/reporting.py
$ sed -n '1,160p' 02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo/08-report.md
```

이 시점의 핵심 코드는 markdown report를 findings, exceptions, remediations 세 섹션으로 나누는 부분이었다.

```python
    lines = [
        "# Cloud Security Control Plane Report",
        "",
        "## Findings",
    ]
```

처음엔 JSON 하나로 끝내도 될 줄 알았지만, 나중에 보니 사람이 읽는 운영 산출물은 markdown report여야 각 finding, suppression, remediation의 현재 상태를 한 번에 설명할 수 있다. 이 단순한 헤더 구성이 capstone의 “플랫폼처럼 보이는 마지막 단계”를 만든다.
