# crypto-primitives-in-practice

## 프로젝트 한줄 소개

hash, MAC, KDF를 같은 “암호학 함수”로 뭉뚱그리지 않고, 각자의 역할을 reference vector 기반으로 검증하는 작은 CLI 랩입니다.

## 왜 배우는가

보안 문서에서 `hash`, `sign`, `encrypt`, `token`, `derive`가 한 문단에 섞이면 설명이 빠르게 흐려집니다.
이 프로젝트는 SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1을 각각 다른 질문으로 분리해,
어떤 입력이 secret이고 어떤 출력이 무엇을 증명하는지 코드와 fixture로 정리합니다.

## 현재 구현 범위

- SHA-256 digest reference vector 검증
- HMAC-SHA256 reference vector 검증
- HKDF-SHA256 reference vector 검증
- PBKDF2-HMAC-SHA1 reference vector 검증
- `check-vectors`와 `demo` CLI

## 빠른 시작

아래 명령은 `security-core` 레포 루트 기준입니다.

```bash
make venv
make demo-crypto
PYTHONPATH=study/Foundations-Security/crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
  study/Foundations-Security/crypto-primitives-in-practice/problem/data/sha256_vectors.json
```

## 검증 명령

```bash
make test-unit
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)
- [guides/security/crypto-primitives.md](../../../../guides/security/crypto-primitives.md)

## 포트폴리오 확장 힌트

primitive 개수를 늘리는 것보다 “왜 plain hash로는 인증이 안 되고, 왜 password KDF와 key expansion KDF를 분리해야 하는가”를
예제와 함께 설명하는 편이 더 설득력 있습니다.

## 알려진 한계

- Argon2id, scrypt, AEAD, digital signature는 현재 범위 밖입니다.
- RFC vector 재현성을 위해 PBKDF2-HMAC-SHA1을 사용하지만, production 기본값으로 추천하는 password KDF는 아닙니다.
- nonce 생성, entropy 수집, key rotation 정책은 후속 프로젝트에서 다룹니다.

