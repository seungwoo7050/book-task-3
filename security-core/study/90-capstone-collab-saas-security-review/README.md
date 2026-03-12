# collab-saas-security-review

## 이 프로젝트의 문제

개별 랩에서 finding을 하나씩 설명할 수 있어도, 실제 운영에서는 무엇을 먼저 고칠지 한 흐름으로 합쳐 말해야 합니다. 이 capstone은 crypto, auth, backend, dependency 판단을 하나의 remediation board와 artifact 세트로 다시 묶는 문제를 다룹니다.

## 내가 만든 답

- `JSON bundle -> consolidated review -> remediation board -> report/artifacts` 파이프라인
- `CRYPTO-*`, `AUTH-*`, `OWASP-*`, dependency `P1`~`P4`를 한 review JSON으로 재구성하는 builder
- `review`와 `demo` CLI로 통합 결과와 demo artifact 세트를 생성하는 도구

## 검증 명령

```bash
make test-capstone
make demo-capstone
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli review \
  study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json
```

## 입출력 계약

- 입력: `problem/data/review_bundle.json`, `problem/data/secure_baseline_bundle.json`, `problem/data/demo_bundle.json`
- 출력: `service`, `summary`, `crypto_findings`, `auth_findings`, `backend_findings`, `dependency_items`, `remediation_board`
- demo 산출물: `.artifacts/capstone/demo/01-service-profile.json`부터 `07-report.md`까지 7개 파일

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [docs/README.md](docs/README.md)
3. [docs/demo-walkthrough.md](docs/demo-walkthrough.md)
4. [python/README.md](python/README.md)
5. [notion/README.md](notion/README.md)

## 배운 점과 한계

- 취약점 개수보다 어떤 finding을 왜 `P1`로 올리고 어떤 항목은 유예 가능한지 설명하는 편이 더 중요합니다.
- 실제 API 서버, DB, queue, 외부 advisory API는 구현하지 않습니다.
- 앞선 foundations 패키지를 import하지 않고 vocabulary만 다시 구현합니다.
