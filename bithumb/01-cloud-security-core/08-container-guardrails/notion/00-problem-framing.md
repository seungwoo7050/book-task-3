# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

컨테이너 보안을 배우려면 반드시 EKS 클러스터가 필요한가? 이 프로젝트의 답은 “그렇지 않다”입니다.
manifest와 이미지 메타데이터만 읽어도, 실제 감사에서 자주 보는 위험 설정을 상당수 재현할 수 있습니다.

## 실제 입력과 출력

입력:
- `insecure_k8s.yaml`, `secure_k8s.yaml`
- `insecure_image.json`, `secure_image.json`

출력:
- `K8S-001` ~ `K8S-005`
- `IMG-001` ~ `IMG-003`
- manifest/image 두 소스에서 나온 finding 목록

## 강한 제약

- PodSecurity Admission 전체, NetworkPolicy, RBAC, Helm/Kustomize는 다루지 않습니다.
- 실제 이미지를 pull하거나 레이어 분석을 하지 않습니다.
- 대신 manifest와 image metadata만으로 설명 가능한 위험에 집중합니다.

## 완료로 보는 기준

- insecure 입력에서 여덟 개 규칙이 모두 발동해야 합니다.
- secure 입력에서는 finding이 0건이어야 합니다.
- Deployment의 `template.spec` 경로를 제대로 읽는지 설명할 수 있어야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)
