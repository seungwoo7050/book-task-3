# 08 Container Guardrails — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.

---

## 1단계: 환경 준비

```bash
cd study2
make venv
```

이 과제에서 추가로 필요한 패키지: `PyYAML` (이미 `pyproject.toml`에 포함).

### PyYAML 설치 확인

```bash
.venv/bin/python -c "import yaml; print(yaml.__version__)"
```

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
08-container-guardrails/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── container-guardrails.md
│   └── references/
│       └── README.md
├── problem/
│   ├── README.md
│   └── data/
│       ├── insecure_image.json
│       ├── insecure_k8s.yaml
│       ├── secure_image.json
│       └── secure_k8s.yaml
└── python/
    ├── README.md
    ├── src/
    │   └── container_guardrails/
    │       ├── __init__.py
    │       ├── cli.py
    │       └── scanner.py
    └── tests/
        └── test_scanner.py
```

```bash
mkdir -p 01-cloud-security-core/08-container-guardrails/{docs/{concepts,references},problem/data,python/{src/container_guardrails,tests}}
```

---

## 3단계: fixture 데이터 작성

### insecure_k8s.yaml

모든 K8S 규칙이 발동하는 Kubernetes manifest:
- `hostPath` 볼륨 마운트
- `image: nginx:latest` (latest 태그)
- `securityContext.privileged: true`
- `securityContext.runAsUser: 0` (root)
- `capabilities.add: ["ALL"]`

### secure_k8s.yaml

안전한 설정의 manifest:
- 볼륨 없음 (또는 emptyDir)
- 특정 태그 사용 (`nginx:1.25`)
- `privileged: false`
- `runAsUser: 1000` (non-root)
- capabilities 추가 없음

### insecure_image.json

```json
{
  "image": "myapp:latest",
  "run_as_root": true,
  "capabilities": ["ALL"]
}
```

### secure_image.json

```json
{
  "image": "myapp:1.2.0",
  "run_as_root": false,
  "capabilities": []
}
```

---

## 4단계: 핵심 스캐너 구현

### scanner.py 작성

구현 순서:

1. **Finding 데이터 클래스** — 과제 04, 05와 동일한 7개 필드

2. **scan_manifest() 함수**
   - `yaml.safe_load_all`로 multi-document YAML 파싱
   - Deployment의 경우 `spec.template.spec`으로 한 단계 더 내려감
   - volumes에서 `hostPath` 검색 → K8S-001
   - containers 순회:
     - image 태그 검사 → K8S-002
     - securityContext.privileged → K8S-003
     - securityContext.runAsUser → K8S-004 (0이거나 미설정)
     - capabilities.add에 "ALL" → K8S-005

3. **scan_image_metadata() 함수**
   - JSON 로드 후 세 가지 필드 검사:
     - latest 태그 → IMG-001
     - `run_as_root: true` → IMG-002
     - capabilities에 "ALL" → IMG-003

4. **as_dicts() 유틸**

### cli.py 작성

manifest YAML 경로와 image JSON 경로를 받아서 combined findings 출력.

```bash
touch python/src/container_guardrails/__init__.py
```

---

## 5단계: 테스트 작성

### test_scanner.py

두 가지 테스트:

1. **insecure inputs → 8개 규칙 전부 발동**
   - manifest 5개 + image 3개 = 8개 control_id
   - `controls == {"K8S-001", "K8S-002", "K8S-003", "K8S-004", "K8S-005", "IMG-001", "IMG-002", "IMG-003"}`

2. **secure inputs → finding 없음**
   - `findings == []`

---

## 6단계: 실행과 검증

### CLI 실행

```bash
cd python
PYTHONPATH=src python -m container_guardrails.cli ../problem/data/insecure_k8s.yaml ../problem/data/insecure_image.json
```

### secure inputs 확인

```bash
PYTHONPATH=src python -m container_guardrails.cli ../problem/data/secure_k8s.yaml ../problem/data/secure_image.json
```

빈 배열 `[]`이 출력되어야 한다.

### 테스트 실행

```bash
cd study2
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

또는:
```bash
make test-unit
```

---

## 환경 요약

| 항목 | 값 |
|------|-----|
| Python | 3.13+ |
| 핵심 의존성 | PyYAML, typer |
| 테스트 프레임워크 | pytest |
| AWS 계정 필요 여부 | 불필요 |
| K8s 클러스터 필요 여부 | 불필요 |
| 외부 서비스 의존 | 없음 |
| 테스트 카테고리 | Unit |

---

## 주의사항

- `yaml.safe_load_all`을 사용하므로, YAML에 `---` 구분자로 여러 document가 있어도 전부 처리된다.
- `runAsUser`가 명시되지 않은 경우 기본값 `0`(root)으로 간주한다.
  이는 보수적(conservative) 판단이며, 실제로는 이미지의 `USER` 지시어에 따라 다를 수 있다.
- `scan_manifest`와 `scan_image_metadata`는 독립적이다.
  manifest만 있으면 manifest만, image JSON만 있으면 image만 검사 가능하다.
