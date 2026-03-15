# 08 Container Guardrails 읽기 지도

이 lab은 실제 클러스터나 admission controller 없이도 manifest와 image metadata만으로 설명 가능한 보안 규칙을 세우는 scanner다. 읽을 때는 "컨테이너 보안 전부"가 아니라, `정적 입력만으로 어디까지 판단하고 어디서 멈추는가`를 먼저 붙드는 편이 정확하다.

## 먼저 붙들 질문
- manifest만 읽고도 확실히 말할 수 있는 위험은 무엇인가?
- 왜 같은 `latest`나 root 신호가 manifest와 image metadata에서 각각 별도 finding으로 남는가?
- secure fixture 0건은 단순 부가 테스트가 아니라 어떤 경계를 고정하는가?

## 이 글은 이렇게 읽으면 된다
1. `scan_manifest()`를 먼저 본다. Deployment template까지 내려가 어떤 K8S control을 만드는지 확인한다.
2. 그다음 `scan_image_metadata()`를 본다. 이미지 단에서 같은 위험을 어떻게 다시 표현하는지 본다.
3. 마지막으로 insecure/secure fixture와 pytest를 본다. 어떤 입력이 8건을 만들고, 어떤 입력이 완전히 0건이 되는지 확인한다.

## 특히 눈여겨볼 장면
- manifest scanner는 `spec.template.spec`를 평탄화해서 Deployment와 Pod를 모두 다룬다.
- `runAsUser`가 없으면 기본값 `0`으로 간주돼 `K8S-004`가 발생한다.
- manifest finding의 `resource_id`는 workload 이름이고, image finding의 `resource_id`는 이미지 문자열이라 triage 축이 다르다.
- scanner는 `containers`만 보고 `initContainers`나 `ephemeralContainers`는 아직 보지 않는다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md)

## 이번 문서의 근거
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/container-guardrails.md`
- `problem/data/insecure_k8s.yaml`
- `problem/data/insecure_image.json`
- `problem/data/secure_k8s.yaml`
- `problem/data/secure_image.json`
- `python/src/container_guardrails/scanner.py`
- `python/src/container_guardrails/cli.py`
- `python/tests/test_scanner.py`
