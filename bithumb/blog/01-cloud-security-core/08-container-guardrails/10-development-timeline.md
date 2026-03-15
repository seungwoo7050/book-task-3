# 08 Container Guardrails: 클러스터 없이 어디까지 판단할 수 있는가

이 lab은 컨테이너 보안을 "실제 EKS를 띄워야만 배울 수 있는 것"으로 다루지 않는다. 대신 manifest와 image metadata만 읽고도 꽤 많은 위험을 설명할 수 있다는 전제에서 출발한다. 그래서 chronology도 플랫폼 통합보다, 어떤 정적 입력을 근거로 어떤 finding을 만들었는지에 맞춰 읽는 편이 자연스럽다.

## 구현 순서 요약
1. manifest에서 설명 가능한 위험을 먼저 추렸다.
2. image metadata를 붙여 같은 위험을 다른 evidence source로 다시 읽었다.
3. secure fixture 0건으로 scanner의 경계를 닫았다.

## Phase 1. manifest만으로도 설명 가능한 위험을 먼저 고정했다

`scan_manifest()`는 이 lab의 태도를 분명하게 보여 준다. YAML을 읽고, `spec.template.spec`가 있으면 Deployment template 안으로 내려가고, 없으면 현재 `spec`를 그대로 본다. 즉 "클러스터가 어떻게 실행할까"를 추론하기보다, manifest 파일에 명시된 것만 근거로 삼겠다는 선택이다.

이 기준에서 첫 번째로 잡는 것은 `hostPath` volume이다. insecure fixture에서는 `/var/run/docker.sock` hostPath가 있고, 이게 곧바로 `K8S-001`이 된다. 그다음 container loop 안에서 `:latest`, `privileged`, `runAsUser == 0`, `capabilities.add`의 `ALL`을 각각 `K8S-002`부터 `K8S-005`로 나눈다. 모두 runtime 없이도 설명 가능한 규칙들이다.

이번 CLI 재실행 결과도 이 구조를 그대로 보여 줬다. manifest 쪽에서만 `K8S-001`부터 `K8S-005`까지 다섯 건이 나왔고, `resource_id`는 모두 workload 이름 `insecure-api`로 묶였다. 즉 triage의 기준축은 "어느 Deployment가 문제인가"다.

## Phase 2. image metadata를 붙여 evidence 축을 하나 더 만들었다

다음 단계는 이미지 자체를 manifest와 분리해서 읽는 일이었다. `scan_image_metadata()`는 이미지 JSON에서 `latest`, `run_as_root`, `capabilities=["ALL"]`를 각각 `IMG-001`, `IMG-002`, `IMG-003`로 만든다. 결과적으로 insecure fixture는 총 8건이 된다.

여기서 중요한 건 중복처럼 보이는 finding을 없애지 않는다는 점이다. `nginx:latest`는 manifest에서도 `K8S-002`, image metadata에서도 `IMG-001`로 잡힌다. root 실행도 `K8S-004`와 `IMG-002`가 둘 다 남는다. 이 scanner는 dedupe보다 source separation을 택한 셈이다. "워크로드 정의가 위험한가"와 "이미지 속성이 위험한가"를 분리해서 보여 주려는 의도다.

이번 CLI 출력에서도 이 차이는 분명했다.

- manifest findings: `resource_id = insecure-api`
- image findings: `resource_id = nginx:latest`

같은 문제처럼 보여도 운영적으로는 remediation 위치가 다를 수 있으니, 이 분리는 꽤 실용적이다.

## Phase 3. secure fixture 0건으로 scanner의 경계를 닫았다

좋은 guardrail은 많이 잡는 것만으로 충분하지 않다. 안전한 입력을 조용히 통과시키는지도 중요하다. 이 lab은 그 점을 `test_secure_inputs_report_no_findings()`로 못 박는다. secure manifest와 secure image metadata를 함께 넣으면 결과는 반드시 `[]`여야 한다.

이번 Todo에서는 그 happy path도 다시 확인했다. 보조 재실행에서 secure fixture 조합은 실제로 빈 배열을 돌려줬다. 그리고 pytest도 다음처럼 통과했다.

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python \
-m pytest \
/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python/tests
```

```text
..                                                                       [100%]
2 passed in 0.02s
```

이 테스트 구조 덕분에 이 scanner는 "무조건 경고를 많이 뿌리는 도구"가 아니라, 적어도 제공된 학습 범위 안에서는 경계를 가진 rule set로 읽을 수 있다.

## 이번에 직접 확인한 rule semantics

소스만 보면 지나치기 쉬운 부분도 하나 있었다. `runAsUser` 판단은 `int(security_context.get("runAsUser", 0)) == 0`이기 때문에, 값을 명시하지 않아도 기본적으로 root로 간주한다. 실제로 임시 Pod manifest에서 `runAsUser`를 생략하고 재실행했더니 `K8S-004`가 바로 나왔다.

이건 꽤 중요한 현재 semantics다. "명시적으로 root"만 잡는 게 아니라, "명시가 없어서 root일 가능성이 열려 있는 상태"도 위험으로 본다는 뜻이기 때문이다.

동시에 범위도 선명하다. scanner는 `containers`만 보고, `initContainers`, `ephemeralContainers`, pod-level `securityContext`는 아직 해석하지 않는다. 그래서 이 lab을 PodSecurity 전체 재현으로 읽으면 과장이고, 정적 입력 기반의 작은 guardrail set로 읽어야 맞다.

## 지금 상태에서 분명한 한계

- Kubernetes surface 일부만 본다.
- deduplication과 suppression이 없다.
- severity는 고정 상수라 context를 반영하지 않는다.
- runtime event나 admission decision은 없다.

그래도 이 lab의 가치는 분명하다. 클러스터 없이도 manifest와 image metadata만으로 납득 가능한 위험을 꽤 많이 설명할 수 있고, 그 결과를 source별 finding으로 분리해 남길 수 있다는 점을 아주 작은 코드로 보여 주기 때문이다.
