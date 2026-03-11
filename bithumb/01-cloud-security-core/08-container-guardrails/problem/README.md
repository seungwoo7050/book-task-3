# 문제 정리

## 원래 문제

EKS나 대형 플랫폼 없이도 학습할 수 있도록, Kubernetes manifest와 이미지 메타데이터 자체를 검사하는 guardrail 엔진을 만들어야 합니다.
핵심은 manifest 수준에서 충분히 설명 가능한 위험과 범위 밖을 명확히 나누는 것입니다.

## 제공된 자료

- `problem/data/insecure_k8s.yaml`
- `problem/data/insecure_image.json`
- `problem/data/secure_k8s.yaml`
- `problem/data/secure_image.json`

## 제약

- 실제 클러스터, admission controller, 런타임 이벤트는 다루지 않습니다.
- manifest와 image metadata에서 설명 가능한 규칙만 다룹니다.

## 통과 기준

- insecure fixture에서 `K8S-*`, `IMG-*` finding이 나와야 합니다.
- secure fixture에서 0건이 보장되어야 합니다.
- finding 출력에 control ID, severity, evidence가 포함되어야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- PodSecurity admission 전체 재현
- 런타임 탐지
- 실제 EKS 연동
