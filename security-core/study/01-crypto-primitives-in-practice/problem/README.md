# 문제 정의

## 문제

`hash`, `MAC`, `KDF`를 같은 보안 함수처럼 다루지 않고, 각 primitive의 입력과 목적을 reference vector로 검증 가능한 형태로 분리해야 합니다.

## 성공 기준

- SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector가 모두 통과해야 합니다.
- `check-vectors <manifest>`가 primitive별 결과를 JSON으로 출력해야 합니다.
- `demo <profile>`가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다.

## canonical validation

```bash
make test-unit
make demo-crypto
```

## 제공 fixture

- `problem/data/sha256_vectors.json`
- `problem/data/hmac_sha256_vectors.json`
- `problem/data/hkdf_sha256_vectors.json`
- `problem/data/pbkdf2_hmac_sha1_vectors.json`
- `problem/data/demo_profile.json`

## provenance

- HKDF vector: RFC 5869 test case 1
- PBKDF2 vector: RFC 6070 test case 1, 2
- SHA-256, HMAC-SHA256: well-known reference vector를 JSON manifest로 재구성
