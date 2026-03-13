# crypto-primitives-in-practice blog

이 디렉터리는 `crypto-primitives-in-practice`를 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 README, problem statement, 개념 문서, Python 구현, pytest, 실제 CLI 출력만으로 복원했다.

## source set

- [../../01-crypto-primitives-in-practice/README.md](../../01-crypto-primitives-in-practice/README.md)
- [../../01-crypto-primitives-in-practice/problem/README.md](../../01-crypto-primitives-in-practice/problem/README.md)
- [../../01-crypto-primitives-in-practice/problem/data/sha256_vectors.json](../../01-crypto-primitives-in-practice/problem/data/sha256_vectors.json)
- [../../01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json](../../01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json)
- [../../01-crypto-primitives-in-practice/problem/data/demo_profile.json](../../01-crypto-primitives-in-practice/problem/data/demo_profile.json)
- [../../01-crypto-primitives-in-practice/docs/README.md](../../01-crypto-primitives-in-practice/docs/README.md)
- [../../01-crypto-primitives-in-practice/docs/concepts/hash-vs-mac-vs-kdf.md](../../01-crypto-primitives-in-practice/docs/concepts/hash-vs-mac-vs-kdf.md)
- [../../01-crypto-primitives-in-practice/python/README.md](../../01-crypto-primitives-in-practice/python/README.md)
- [../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py](../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py)
- [../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/vectors.py](../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/vectors.py)
- [../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/cli.py](../../01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/cli.py)
- [../../01-crypto-primitives-in-practice/python/tests/test_primitives.py](../../01-crypto-primitives-in-practice/python/tests/test_primitives.py)
- [../../01-crypto-primitives-in-practice/python/tests/test_cli.py](../../01-crypto-primitives-in-practice/python/tests/test_cli.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-primitives-vectors-and-demo-contract.md](10-chronology-primitives-vectors-and-demo-contract.md)
3. [../../01-crypto-primitives-in-practice/README.md](../../01-crypto-primitives-in-practice/README.md)

## 검증 진입점

```bash
cd ../../..
make venv
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m pytest study/01-crypto-primitives-in-practice/python/tests
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
  study/01-crypto-primitives-in-practice/problem/data/sha256_vectors.json
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli demo \
  study/01-crypto-primitives-in-practice/problem/data/demo_profile.json
```

## chronology 메모

- git anchor가 하루치라서 chronology는 `primitive 경계 고정 -> manifest evaluator -> demo contract` 순으로 재구성했다.
- 핵심 전환점은 `hash`와 `MAC`를 따로 구현하는 데서 끝나지 않고, manifest encoding과 deterministic demo까지 하나의 계약으로 묶은 지점이다.
