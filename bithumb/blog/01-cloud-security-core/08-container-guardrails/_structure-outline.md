# 08 Container Guardrails 구조 메모

## 이번 문서의 중심
- 컨테이너 보안을 "클러스터 연동"이 아니라 "정적 입력 기반 guardrail"로 설명한다.
- 서사는 `manifest 위험 -> image metadata 분리 -> secure 0건` 순서로 둔다.
- duplicate-looking findings를 버그처럼 쓰지 않고 source separation으로 해석한다.

## 먼저 붙들 소스
- `../../../01-cloud-security-core/08-container-guardrails/README.md`
- `../../../01-cloud-security-core/08-container-guardrails/problem/README.md`
- `../../../01-cloud-security-core/08-container-guardrails/python/README.md`
- `../../../01-cloud-security-core/08-container-guardrails/docs/concepts/container-guardrails.md`
- `../../../01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml`
- `../../../01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json`
- `../../../01-cloud-security-core/08-container-guardrails/problem/data/secure_k8s.yaml`
- `../../../01-cloud-security-core/08-container-guardrails/problem/data/secure_image.json`
- `../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py`
- `../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/cli.py`
- `../../../01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py`

## 본문 배치
- 도입
  - 실제 클러스터 없이도 설명 가능한 위험을 다루는 lab이라는 점을 먼저 둔다.
- Phase 1
  - `spec.template.spec` flattening, `hostPath`, `latest`, `privileged`, `runAsUser`, `ALL capabilities`를 설명한다.
- Phase 2
  - image metadata scanner를 붙여 K8S/IMG control이 서로 다른 evidence axis라는 점을 보여 준다.
- Phase 3
  - secure fixture 0건과 pytest 통과로 noise floor를 정리한다.
- 마무리
  - `runAsUser` 기본값 semantics, `initContainers` 미지원, dedupe 부재를 한계로 남긴다.

## 꼭 남길 검증 신호
- CLI insecure 출력 8건
- secure fixture 보조 재실행 결과 `[]`
- pytest `2 passed in 0.02s`
- 임시 manifest 재실행에서 `runAsUser` 미지정 시 `K8S-004` 발생

## 탈락 기준
- "컨테이너 보안 전체"처럼 과장하면 안 된다.
- manifest/image 중복 신호를 설명 없이 나열하면 안 된다.
- secure fixture 0건의 의미를 빼먹으면 scanner 경계가 흐려진다.
