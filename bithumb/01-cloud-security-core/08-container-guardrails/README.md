# 08 Container Guardrails

## 풀려는 문제

클러스터를 직접 띄우지 않아도 manifest와 image metadata만으로 충분히 배울 수 있는 컨테이너 보안 규칙이 있습니다.
이 프로젝트는 Kubernetes manifest와 image metadata에서 위험 설정을 찾는 guardrail scanner를 구현합니다.

## 내가 낸 답

- Kubernetes manifest에서 `hostPath`, `privileged`, `runAsRoot`, broad capability 같은 위험 설정을 검사합니다.
- image metadata에서 `latest` tag, root 실행, `ALL` capability 같은 위험 신호를 추가로 해석합니다.
- manifest와 image metadata 결과를 각각 설명 가능한 finding으로 반환합니다.
- secure fixture 0건 시나리오를 함께 두어 규칙의 기준선을 분명하게 만듭니다.

## 입력과 출력

- 입력: `problem/data/insecure_k8s.yaml`, `problem/data/insecure_image.json`, secure fixture 쌍
- 출력: `K8S-*`, `IMG-*` control ID를 가진 guardrail finding 목록

## 검증 방법

```bash
make venv
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

## 현재 상태

- `verified`
- insecure/secure fixture 쌍과 설명 가능한 finding 출력이 준비되어 있습니다.
- 10번 캡스톤이 이 scanner를 k8s 입력 처리 경로에서 재사용합니다.

## 한계와 다음 단계

- PodSecurity admission 전체를 재현하지는 않습니다.
- 런타임 이벤트, admission controller, 실제 클러스터 연동은 범위 밖입니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)
