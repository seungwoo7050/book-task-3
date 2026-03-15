# 08 Container Guardrails 근거 정리

이 문서는 manifest scanner가 무엇을 하는지보다, 어떤 근거 때문에 이 규칙들을 "설명 가능한 guardrail"이라고 부를 수 있는지를 묶어 두는 메모다. 특히 이번 lab은 fixture가 매우 작아서, 테스트가 덮는 범위와 코드만 보면 드러나는 semantics를 분리해서 적는 편이 중요했다.

## Phase 1. manifest scanner는 정적 파일에서 바로 읽히는 위험만 고른다

- 당시 목표: 클러스터 없이도 manifest에서 설명 가능한 고위험 설정을 먼저 고른다.
- 핵심 근거:
  - `scan_manifest()`는 YAML multi-document를 순회한다.
  - `spec.template.spec`가 있으면 그 안으로 내려가고, 없으면 현재 `spec`를 그대로 본다.
  - `volumes` 안 `hostPath`는 `K8S-001`
  - `containers` loop 안에서 `:latest`, `privileged`, `runAsUser == 0`, `capabilities.add`에 `ALL`을 각각 별도 control로 만든다.
- 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python -m container_guardrails.cli /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json`
- 검증 신호:
  - insecure fixture는 `K8S-001`부터 `K8S-005`까지 전부 발생했다.
  - 첫 manifest finding의 `resource_id`는 workload 이름 `insecure-api`였다.
- 해석:
  - 이 scanner는 admission controller를 흉내 내지 않고, 정적 파일만 보고도 설명 가능한 위험을 좁게 고른다.

## Phase 2. 같은 위험이라도 manifest와 image metadata를 분리해서 남긴다

- 당시 목표: workload 설정과 이미지 속성을 섞지 않고, 같은 위험도 source를 나눠 남긴다.
- 핵심 근거:
  - `scan_manifest()`의 `K8S-002`는 container image string이 `:latest`인지 본다.
  - `scan_image_metadata()`의 `IMG-001`도 image JSON이 `:latest`인지 다시 본다.
  - root 실행과 `ALL` capability도 manifest와 image metadata에서 각각 별도 control로 나뉜다.
  - image finding의 `resource_id`는 이미지 문자열 `nginx:latest`다.
- 재실행:
  - CLI 출력에서 `K8S-*` 5건과 `IMG-*` 3건, 총 8건을 다시 확인했다.
- 검증 신호:
  - 같은 insecure fixture라도 `latest`는 `K8S-002`와 `IMG-001` 두 경로로 모두 잡힌다.
  - root 신호도 `K8S-004`와 `IMG-002`로 따로 남는다.
- 해석:
  - 이 scanner는 dedupe를 하지 않는다. 대신 "manifest가 위험한가"와 "image가 위험한가"를 다른 evidence axis로 남긴다.

## Phase 3. secure fixture 0건이 noise floor를 잠근다

- 당시 목표: scanner가 noisy rule dump가 아니라, 안전한 입력은 조용히 통과시키는 guardrail임을 보인다.
- 핵심 근거:
  - `test_insecure_inputs_report_expected_findings()`는 8개 control set를 정확히 비교한다.
  - `test_secure_inputs_report_no_findings()`는 secure fixture 조합에서 `[]`를 요구한다.
  - 이번 보조 재실행에서도 secure 조합은 실제로 빈 배열이었다.
- 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python -m pytest /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python/tests`
- 검증 신호:
  - `2 passed in 0.02s`
  - secure pair에 대한 보조 재실행 결과는 `[]`
- 해석:
  - 좋은 guardrail은 많이 잡는 것만큼, 잡지 말아야 할 입력을 조용히 넘기는 것도 중요하다.

## 이번 Todo에서 추가로 확인한 semantics

- `runAsUser`가 없으면 `security_context.get("runAsUser", 0)` 때문에 기본값 `0`으로 처리돼 `K8S-004`가 발생한다.
- 실제로 임시 Pod manifest에서 `runAsUser`를 생략한 채 재실행했더니 `missing-user` workload에 대해 `K8S-004`가 나왔다.
- scanner는 `containers`만 순회하므로 `initContainers`, `ephemeralContainers`, pod-level `securityContext`는 현재 범위 밖이다.

## 이번 Todo에서 남긴 한계

- deduplication이나 suppression이 없다.
- Kubernetes 문서 전체를 해석하지 않고 일부 필드만 본다.
- severity는 rule별 상수라 context-aware risk scoring이 없다.
