# collab-saas-security-review

## 프로젝트 한줄 소개

multi-tenant collaboration SaaS API를 가정하고, crypto/auth/backend/dependency 판단을 하나의 remediation board로 묶는 offline security review capstone입니다.

## 왜 배우는가

개별 랩에서 finding을 하나씩 설명할 수 있어도, 실제 운영에서는 무엇을 먼저 고칠지 한 흐름으로 합쳐 말해야 합니다.
이 capstone은 JSON bundle 하나로 서비스 프로필, auth 설계, backend route 경계, dependency queue를 함께 읽고
consolidated review와 artifact report를 생성합니다.

## 현재 구현 범위

- `JSON bundle -> consolidated review -> remediation board -> demo artifacts` 파이프라인
- `CRYPTO-001`~`CRYPTO-004`와 기존 `AUTH-*`, `OWASP-*`, dependency triage priority 재구성
- `review`와 `demo` CLI
- `.artifacts/capstone/demo/` artifact 세트 생성

## 빠른 시작

아래 명령은 `security-core` 레포 루트 기준입니다.

```bash
make venv
make test-capstone
make demo-capstone
PYTHONPATH=study/Capstone/collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli review \
  study/Capstone/collab-saas-security-review/problem/data/review_bundle.json
```

## 검증 명령

```bash
make test-unit
make test-capstone
make demo-capstone
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [docs/demo-walkthrough.md](docs/demo-walkthrough.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

취약점 개수를 늘리는 것보다 어떤 finding을 왜 `P1`로 올리고, 어떤 항목은 문서화 후 만료시켜도 되는지 remediation board 기준으로 설명하는 편이 더 설득력 있습니다.

## 알려진 한계

- 실제 API 서버, DB, queue, 외부 advisory API는 구현하지 않습니다.
- 앞선 foundations 프로젝트 패키지를 import하지 않고 동일 vocabulary를 다시 구현합니다.
- tenant isolation runtime enforcement나 production 배포 자동화는 현재 범위 밖입니다.
