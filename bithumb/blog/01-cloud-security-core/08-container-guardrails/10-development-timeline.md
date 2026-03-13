# 08 Container Guardrails: manifest와 image metadata로 guardrail 세우기

실제 클러스터 없이도 manifest와 image metadata만으로 설명 가능한 컨테이너 보안 규칙을 만드는 scanner다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "클러스터 없이도 어떤 manifest 규칙은 충분히 설명 가능한가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. manifest에서 `hostPath`, `latest`, `privileged`, `runAsRoot`, broad capability를 읽는 규칙을 만들었다.
2. image metadata 쪽에서도 같은 위험 신호를 별도 source로 스캔했다.
3. secure fixture 0건 테스트로 scanner의 상한선을 분명히 했다.

## Phase 1. manifest에서 설명 가능한 위험 설정을 먼저 골랐다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `manifest에서 설명 가능한 위험 설정을 먼저 골랐다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 클러스터 없이도 static file만 읽고 설명할 수 있는 규칙을 고른다.
- 변경 단위: `python/src/container_guardrails/scanner.py`의 `scan_manifest`
- 처음 가설: 좋은 학습용 guardrail은 admission controller 전체를 흉내 내기보다, manifest만 보고도 납득할 수 있는 몇 개 위험 설정에 집중하는 편이 낫다.
- 실제 진행: scanner는 `spec.template.spec`까지 내려가 pod template를 평탄화한 뒤, `hostPath` volume 사용 여부를 먼저 확인했다. 그 다음 container 단위로 image tag와 securityContext를 읽는 구조를 세웠다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json
```

검증 신호:
- CLI 첫 finding이 바로 `K8S-001` hostPath volume 사용이었다.
- resource_id가 `insecure-api`로 고정돼 later triage가 쉬워졌다.

핵심 코드:

```python
def scan_manifest(manifest_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    docs = list(yaml.safe_load_all(manifest_path.read_text()))
    for document in docs:
        if not isinstance(document, dict):
            continue
        metadata = document.get("metadata", {})
        resource_id = metadata.get("name", "unknown") if isinstance(metadata, dict) else "unknown"
        spec = document.get("spec", {})
        if isinstance(spec, dict) and isinstance(spec.get("template"), dict):
            spec = spec["template"].get("spec", {})
        if not isinstance(spec, dict):
            continue

        for volume in spec.get("volumes", []):
            if isinstance(volume, dict) and "hostPath" in volume:
                findings.append(
                    Finding("k8s-manifest", "K8S-001", "HIGH", "volume", str(resource_id), "hostPath volume is used", str(resource_id))
                )
```

왜 이 코드가 중요했는가: manifest를 어떻게 평탄화하느냐가 guardrail의 시작이었다. pod template를 놓치면 실제로 많이 보는 Deployment 형태를 아예 스캔하지 못한다.

새로 배운 것: 컨테이너 보안의 많은 위험은 runtime 전에 이미 manifest에서 읽힌다. static guardrail이 유효한 이유가 여기 있다.

다음: 이제 container-level securityContext 규칙을 더 붙여야 했다.

## Phase 2. securityContext를 broad privilege 신호로 묶었다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `securityContext를 broad privilege 신호로 묶었다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: `latest`, `privileged`, root 실행, `ALL` capability 같은 위험 신호를 container-level finding으로 만든다.
- 변경 단위: `python/src/container_guardrails/scanner.py`의 container loop
- 처음 가설: 주니어도 바로 설명할 수 있는 규칙을 고르면 guardrail의 가치가 더 선명해진다.
- 실제 진행: container loop는 image tag가 `latest`인지, `privileged`가 켜져 있는지, `runAsUser`가 0인지, `ALL` capability가 추가됐는지를 차례대로 검사해 `K8S-002`~`K8S-005`로 분리했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json
```

검증 신호:
- CLI 출력에서 `K8S-002`부터 `K8S-005`까지 네 개 control이 `nginx:latest` evidence와 함께 나왔다.
- manifest source만으로도 root 실행과 broad capability를 설명 가능한 finding으로 남겼다.

핵심 코드:

```python
        for container in spec.get("containers", []):
            if not isinstance(container, dict):
                continue
            image = str(container.get("image", ""))
            security_context = container.get("securityContext", {})
            if not isinstance(security_context, dict):
                security_context = {}

            if image.endswith(":latest"):
                findings.append(
                    Finding("k8s-manifest", "K8S-002", "MEDIUM", "container", str(resource_id), "Container uses latest tag", image)
                )
            if bool(security_context.get("privileged")):
                findings.append(
                    Finding("k8s-manifest", "K8S-003", "HIGH", "container", str(resource_id), "Privileged container is enabled", image)
                )
            if int(security_context.get("runAsUser", 0)) == 0:
                findings.append(
                    Finding("k8s-manifest", "K8S-004", "HIGH", "container", str(resource_id), "Container runs as root", image)
                )
            capabilities = security_context.get("capabilities", {})
            if isinstance(capabilities, dict) and "ALL" in capabilities.get("add", []):
                findings.append(
                    Finding("k8s-manifest", "K8S-005", "HIGH", "container", str(resource_id), "Container adds broad Linux capabilities", image)
                )
    return findings
```

왜 이 코드가 중요했는가: 이 분기들이 들어가면서 scanner는 단순 schema checker가 아니라 실제 guardrail처럼 동작했다. 각각이 서로 다른 수정 행동을 요구하기 때문이다.

새로 배운 것: `privileged`, root 실행, broad capability는 모두 “컨테이너 권한을 과하게 넓힌다”는 공통 축에 있지만, remediation 포인트는 미묘하게 다르다. control을 나누는 이유가 여기 있다.

다음: manifest만으로 끝내지 않고 image metadata도 같은 finding 언어로 읽어야 했다.

## Phase 3. image metadata와 secure fixture 0건으로 경계를 닫았다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `image metadata와 secure fixture 0건으로 경계를 닫았다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: manifest 외부의 이미지 정보도 같은 scanner에서 다루고, 안전한 입력은 조용히 지나가게 한다.
- 변경 단위: `python/src/container_guardrails/scanner.py`의 `scan_image_metadata`, `python/tests/test_scanner.py`
- 처음 가설: manifest와 image metadata를 함께 봐야 설명이 구체적이고, secure fixture 0건이 있어야 noisy scanner가 되지 않는다.
- 실제 진행: image JSON에서도 `latest`, root 실행, `ALL` capability를 `IMG-*` finding으로 만들었다. 테스트는 insecure fixture에서 K8S/IMG control 전체 집합이 나오고, secure fixture에서는 완전히 비어야 한다고 못 박았다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

검증 신호:
- pytest가 `2 passed in 0.04s`로 통과했다.
- `test_secure_inputs_report_no_findings`가 scanner의 noise floor를 제어한다.

핵심 코드:

```python
def test_insecure_inputs_report_expected_findings() -> None:
    findings = scan_manifest(_problem_data("insecure_k8s.yaml")) + scan_image_metadata(_problem_data("insecure_image.json"))
    controls = {finding.control_id for finding in findings}
    assert controls == {"K8S-001", "K8S-002", "K8S-003", "K8S-004", "K8S-005", "IMG-001", "IMG-002", "IMG-003"}


def test_secure_inputs_report_no_findings() -> None:
    findings = scan_manifest(_problem_data("secure_k8s.yaml")) + scan_image_metadata(_problem_data("secure_image.json"))
    assert findings == []
```

왜 이 코드가 중요했는가: guardrail scanner의 신뢰도는 insecure에서 많이 잡는 것보다 secure에서 조용한지로 판가름 난다. 이 테스트가 그 경계를 선명하게 한다.

새로 배운 것: 좋은 guardrail은 “무조건 많이 경고”하지 않는다. source가 여러 개여도 같은 severity/control discipline을 유지해야 운영에 얹기 쉽다.

다음: 다음 프로젝트에서는 finding 이후의 거버넌스, 즉 exception/evidence/audit를 모델링한다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 scanner는 클러스터 없는 학습 환경을 핑계로 대충 축소하지 않았다. manifest와 image metadata에서 바로 설명할 수 있는 위험만 골라 control로 분리했고, secure fixture 0건까지 지켜서 capstone에 그대로 실을 수 있는 guardrail 입력을 만들었다.
