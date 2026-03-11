# 문제 정의

## 문제

백엔드 보안 문서에서 자주 등장하는 `hash`, `MAC`, `KDF`를 같은 단어처럼 쓰지 않고, 각 primitive가 무엇을 입력으로
받고 어떤 목적을 위해 쓰이는지 학습 가능한 작은 CLI를 구현합니다. 결과는 reference vector로 검증 가능해야 하고,
demo 출력만 보고도 secret input과 public input의 차이를 설명할 수 있어야 합니다.

## 성공 기준

- SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1의 reference vector가 통과해야 합니다.
- `check-vectors <manifest>`가 primitive별 결과와 pass/fail 요약을 JSON으로 출력해야 합니다.
- `demo <profile>`가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다.
- 문서가 hash vs MAC vs KDF, password KDF vs key expansion KDF, plain hash의 한계를 분리해서 설명해야 합니다.

## canonical validation

아래 명령은 `security-core` 레포 루트 기준입니다.

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

- HKDF 벡터는 RFC 5869 test case 1을 사용합니다.
- PBKDF2 벡터는 RFC 6070 test case 1, 2를 사용합니다.
- SHA-256과 HMAC-SHA256은 well-known reference vector를 재현 가능한 JSON manifest로 정리합니다.

