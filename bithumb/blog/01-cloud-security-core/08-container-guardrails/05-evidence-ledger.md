# 08 Container Guardrails 근거 정리

실제 클러스터 없이도 manifest와 image metadata만으로 설명 가능한 컨테이너 보안 규칙을 만드는 scanner다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. manifest에서 설명 가능한 위험 설정을 먼저 골랐다

이 구간에서는 `manifest에서 설명 가능한 위험 설정을 먼저 골랐다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: 클러스터 없이도 static file만 읽고 설명할 수 있는 규칙을 고른다.
- 변경 단위: `python/src/container_guardrails/scanner.py`의 `scan_manifest`
- 처음 가설: 좋은 학습용 guardrail은 admission controller 전체를 흉내 내기보다, manifest만 보고도 납득할 수 있는 몇 개 위험 설정에 집중하는 편이 낫다.
- 실제 조치: scanner는 `spec.template.spec`까지 내려가 pod template를 평탄화한 뒤, `hostPath` volume 사용 여부를 먼저 확인했다. 그 다음 container 단위로 image tag와 securityContext를 읽는 구조를 세웠다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json`
- 검증 신호:
  - CLI 첫 finding이 바로 `K8S-001` hostPath volume 사용이었다.
  - resource_id가 `insecure-api`로 고정돼 later triage가 쉬워졌다.
- 핵심 코드 앵커: `01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py:22-40`
- 새로 배운 것: 컨테이너 보안의 많은 위험은 runtime 전에 이미 manifest에서 읽힌다. static guardrail이 유효한 이유가 여기 있다.
- 다음: 이제 container-level securityContext 규칙을 더 붙여야 했다.

## Phase 2. securityContext를 broad privilege 신호로 묶었다

이 구간에서는 `securityContext를 broad privilege 신호로 묶었다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: `latest`, `privileged`, root 실행, `ALL` capability 같은 위험 신호를 container-level finding으로 만든다.
- 변경 단위: `python/src/container_guardrails/scanner.py`의 container loop
- 처음 가설: 주니어도 바로 설명할 수 있는 규칙을 고르면 guardrail의 가치가 더 선명해진다.
- 실제 조치: container loop는 image tag가 `latest`인지, `privileged`가 켜져 있는지, `runAsUser`가 0인지, `ALL` capability가 추가됐는지를 차례대로 검사해 `K8S-002`~`K8S-005`로 분리했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json`
- 검증 신호:
  - CLI 출력에서 `K8S-002`부터 `K8S-005`까지 네 개 control이 `nginx:latest` evidence와 함께 나왔다.
  - manifest source만으로도 root 실행과 broad capability를 설명 가능한 finding으로 남겼다.
- 핵심 코드 앵커: `01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py:42-67`
- 새로 배운 것: `privileged`, root 실행, broad capability는 모두 “컨테이너 권한을 과하게 넓힌다”는 공통 축에 있지만, remediation 포인트는 미묘하게 다르다. control을 나누는 이유가 여기 있다.
- 다음: manifest만으로 끝내지 않고 image metadata도 같은 finding 언어로 읽어야 했다.

## Phase 3. image metadata와 secure fixture 0건으로 경계를 닫았다

이 구간에서는 `image metadata와 secure fixture 0건으로 경계를 닫았다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: manifest 외부의 이미지 정보도 같은 scanner에서 다루고, 안전한 입력은 조용히 지나가게 한다.
- 변경 단위: `python/src/container_guardrails/scanner.py`의 `scan_image_metadata`, `python/tests/test_scanner.py`
- 처음 가설: manifest와 image metadata를 함께 봐야 설명이 구체적이고, secure fixture 0건이 있어야 noisy scanner가 되지 않는다.
- 실제 조치: image JSON에서도 `latest`, root 실행, `ALL` capability를 `IMG-*` finding으로 만들었다. 테스트는 insecure fixture에서 K8S/IMG control 전체 집합이 나오고, secure fixture에서는 완전히 비어야 한다고 못 박았다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests`
- 검증 신호:
  - pytest가 `2 passed in 0.04s`로 통과했다.
  - `test_secure_inputs_report_no_findings`가 scanner의 noise floor를 제어한다.
- 핵심 코드 앵커: `01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py:10-18`
- 새로 배운 것: 좋은 guardrail은 “무조건 많이 경고”하지 않는다. source가 여러 개여도 같은 severity/control discipline을 유지해야 운영에 얹기 쉽다.
- 다음: 다음 프로젝트에서는 finding 이후의 거버넌스, 즉 exception/evidence/audit를 모델링한다.
