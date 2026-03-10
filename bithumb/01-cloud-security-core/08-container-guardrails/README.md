# 08 Container Guardrails

## 프로젝트 한줄 소개

Kubernetes manifest와 이미지 메타데이터에서 위험 설정을 찾는 guardrail 스캐너입니다.

## 왜 배우는가

클러스터를 직접 띄우지 않아도 컨테이너 보안의 핵심 위험 설정을 충분히 학습할 수 있습니다. 이 프로젝트는 manifest와 이미지 메타데이터만으로도 설명 가능한 보안 규칙을 만들 수 있다는 점을 보여 줍니다.

## 현재 구현 범위

- Kubernetes manifest를 읽고 위험한 보안 설정을 찾습니다.
- 이미지 메타데이터와 함께 해석해 guardrail finding을 생성합니다.
- manifest 수준에서 설명 가능한 규칙에 집중합니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json
```

## 검증 명령

```bash
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

EKS를 띄우지 않았다는 점을 약점처럼 숨기지 말고, manifest 수준에서 어떤 위험을 충분히 검토할 수 있는지와 범위 밖을 명확히 적는 편이 좋습니다.

## 알려진 한계

- PodSecurity admission 전체를 재현하지는 않습니다.
- 실제 클러스터 런타임 이벤트와 admission controller 연동은 다루지 않습니다.
