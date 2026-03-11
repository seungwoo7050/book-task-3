# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- Kubernetes manifest를 읽고 위험한 보안 설정을 찾습니다.
- 이미지 메타데이터와 함께 해석해 guardrail finding을 생성합니다.
- manifest 수준에서 설명 가능한 규칙에 집중합니다.

## 핵심 엔트리포인트

- `python/src/container_guardrails/scanner.py`
- `python/src/container_guardrails/cli.py`

## 실행

```bash
make venv
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

## 대표 출력 예시

```json
[
  {
    "source": "k8s-manifest",
    "control_id": "K8S-001",
    "severity": "HIGH",
    "resource_type": "volume",
    "resource_id": "insecure-api",
    "title": "hostPath volume is used",
    "evidence_ref": "insecure-api"
  }
]
```

## 구현 메모

scanner는 manifest와 image metadata를 함께 읽어 설명 가능한 finding만 남기도록 설계했습니다.
