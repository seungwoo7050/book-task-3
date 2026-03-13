# 10 Development Timeline

이 문서는 `Container Guardrails`를 현재 manifest fixture, image metadata fixture, scanner 코드만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 admission controller 재현이 아니라, static input만으로 설명 가능한 guardrail을 분리하는 단계인지 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `scanner.py`, `test_scanner.py`를 같이 읽었다.
- 이슈: 처음엔 Kubernetes manifest만 보면 될 줄 알았는데, 실제 문제 정의와 테스트를 보니 image metadata까지 같이 읽어야 `latest`, root, capability 같은 경계를 설명할 수 있었다.
- 판단: 이 프로젝트의 핵심은 클러스터 없이도 충분히 설명 가능한 위험을 모으되, 런타임 탐지와 admission 전체는 일부러 범위 밖으로 남기는 데 있다.

CLI:

```bash
$ sed -n '1,120p' 01-cloud-security-core/08-container-guardrails/problem/README.md
$ sed -n '1,260p' 01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py
$ sed -n '1,200p' 01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py
```

이 시점의 핵심 코드는 manifest의 broad security context를 한 자리에서 읽는 부분이었다.

```python
            if bool(security_context.get("privileged")):
                findings.append(Finding(... control_id="K8S-003", ...))
            if int(security_context.get("runAsUser", 0)) == 0:
                findings.append(Finding(... control_id="K8S-004", ...))
            if isinstance(capabilities, dict) and "ALL" in capabilities.get("add", []):
                findings.append(Finding(... control_id="K8S-005", ...))
```

처음엔 `privileged` 하나만 보면 충분하다고 생각했지만, 실제로는 root 실행과 broad capability가 다른 remediation 문맥을 갖기 때문에 분리된 control ID가 필요했다. 이 조각 덕분에 “컨테이너 권한이 넓다”를 세부 근거로 다시 풀어 설명할 수 있다.

### Session 2

- 진행: CLI와 pytest를 돌려 insecure/secure 경계가 현재도 유지되는지 확인했다.
- 검증: CLI는 `K8S-*`, `IMG-*` 합쳐 8개 finding을 출력했고, pytest는 insecure fixture 8개 control과 secure fixture 0건을 모두 통과했다.
- 판단: 처음 가설은 manifest 규칙만 있으면 데모가 충분하다는 쪽이었지만, 이미지 메타데이터 규칙이 있어야 컨테이너 보안 논의를 런타임 없이도 더 입체적으로 설명할 수 있다.
- 다음: capstone은 여기서 manifest 경로만 받아 간단한 k8s ingestion으로 흡수하고, image metadata까지는 아직 통합하지 않는다.

CLI:

```bash
$ make venv
$ PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json
$ PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

출력:

```text
"control_id": "K8S-001"
"control_id": "IMG-003"
2 passed in 0.02s
```
