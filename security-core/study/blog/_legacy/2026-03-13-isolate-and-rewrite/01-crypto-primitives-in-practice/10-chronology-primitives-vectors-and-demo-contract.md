# 10 Primitives, Vectors, And Demo Contract

이 글은 프로젝트 전체에서 `primitive 구분`과 `검증 계약`이 처음 고정되는 구간이다. 흐름은 `개념 분리 -> vector evaluator -> deterministic demo` 순서로 읽는 편이 실제 코드 표면과 가장 잘 맞는다.

## Day 1
### Session 1

- 당시 목표: `hash`, `MAC`, `KDF`를 말로만 분리하지 않고 함수 표면부터 갈라 놓는다.
- 변경 단위: `python/src/crypto_primitives_in_practice/primitives.py`
- 처음 가설: SHA-256, HMAC, HKDF, PBKDF2를 한 evaluator 안에서 분기해도 충분할 것 같았다.
- 실제 진행: `docs/concepts/hash-vs-mac-vs-kdf.md`를 먼저 읽고, primitive마다 입력이 다르다는 사실을 함수 시그니처 수준으로 드러내는 쪽으로 축을 바꿨다.

CLI:

```bash
$ cd security-core
$ sed -n '1,200p' study/01-crypto-primitives-in-practice/docs/concepts/hash-vs-mac-vs-kdf.md
$ sed -n '1,220p' study/01-crypto-primitives-in-practice/python/src/crypto_primitives_in_practice/primitives.py
```

검증 신호:

- 개념 문서는 hash를 공개 입력 fingerprint, MAC을 secret key가 필요한 무결성 증명, KDF를 새 key material 파생으로 잘라 둔다.
- `primitives.py`도 같은 분리를 따라 `sha256_digest`, `hmac_sha256`, `hkdf_sha256`, `pbkdf2_hmac_sha1`를 별도 함수로 둔다.

핵심 코드:

```python
def sha256_digest(message: bytes) -> str:
    return hashlib.sha256(message).hexdigest()


def hmac_sha256(key: bytes, message: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()
```

왜 이 코드가 중요했는가:

처음부터 `message`만 받는 함수와 `key, message`를 함께 받는 함수를 갈라 놓으니, "plain hash로 인증하면 안 된다"는 문장이 추상 설명이 아니라 호출 규약 차이로 남았다. 이 프로젝트의 방향은 여기서 이미 정해졌다.

같은 결정은 KDF에도 그대로 이어진다.

```python
def pbkdf2_hmac_sha1(password: bytes, salt: bytes, iterations: int, length: int) -> str:
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    if length <= 0:
        raise ValueError("length must be positive")
    return hashlib.pbkdf2_hmac("sha1", password, salt, iterations, length).hex()
```

PBKDF2는 password, salt, iterations를 받는다. HKDF는 ikm, salt, info, length를 받는다. 둘 다 KDF지만 "entropy가 약한 입력을 늘리는가"와 "이미 secret인 재료를 context별로 나누는가"가 다르다는 사실이 함수 인자에서 바로 드러난다.

새로 배운 것:

- KDF를 하나의 범주로만 기억하면 password hardening과 key separation을 섞어 설명하기 쉽다.
- 이 프로젝트에 PBKDF2와 HKDF가 같이 들어 있는 이유는 "KDF 예시를 늘리기 위해서"가 아니라, KDF 내부에서도 질문이 갈라진다는 점을 보여 주기 위해서다.

다음:

- primitive 함수를 만든 뒤에는 vector manifest가 이 구분을 실제 검증 계약으로 고정해 주는지 확인해야 했다.

### Session 2

- 당시 목표: primitive 표면을 reference vector와 직접 연결하는 evaluator를 만든다.
- 변경 단위: `python/src/crypto_primitives_in_practice/vectors.py`
- 처음 가설: manifest마다 별도 파서를 두면 구현이 단순할 것 같았다.
- 실제 진행: `primitive`와 `encoding`만 manifest에서 읽고, 나머지는 `_compute_actual_hex()` 안에서 분기하는 공통 evaluator로 정리했다.

CLI:

```bash
$ sed -n '1,220p' study/01-crypto-primitives-in-practice/problem/data/sha256_vectors.json
$ sed -n '1,220p' study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json
$ PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
    .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
    study/01-crypto-primitives-in-practice/problem/data/sha256_vectors.json
```

검증 신호:

- `sha256_vectors.json`은 기본 `utf-8` 인코딩을 쓰다가 `hex-00010203` 케이스에서만 `encoding: "hex"`로 덮어쓴다.
- 실제 실행 결과는 `passed: 3`, `failed: 0`이고, 빈 문자열과 `abc`, hex payload가 모두 기대 hex와 일치한다.

핵심 코드:

```python
def _decode(value: str, encoding: str) -> bytes:
    if encoding == "utf-8":
        return value.encode()
    if encoding == "hex":
        return bytes.fromhex(value)
    raise ValueError(f"unsupported encoding: {encoding}")


def _encoding(manifest: dict[str, Any], vector: dict[str, Any]) -> str:
    return str(vector.get("encoding", manifest.get("encoding", "utf-8")))
```

왜 이 코드가 중요했는가:

vector를 통과시키는 핵심은 알고리즘 구현보다 입력 decoding을 manifest 계약에 맞추는 일이었다. 이 두 함수가 없으면 같은 SHA-256이라도 `"abc"`와 `"00010203"`를 같은 방식으로 읽어 버리고, reference vector라는 근거가 흐려진다.

evaluator의 중심도 여기로 모인다.

```python
def check_vectors_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    primitive = str(manifest["primitive"])
    results: list[dict[str, Any]] = []

    for vector in manifest["vectors"]:
        actual_hex = _compute_actual_hex(primitive, manifest, vector)
        expected_hex = str(vector["expected_hex"]).lower()
        results.append(
            {
                "name": str(vector["name"]),
                "matched": constant_time_compare(actual_hex, expected_hex),
                "actual_hex": actual_hex,
                "expected_hex": expected_hex,
            }
        )
```

`actual_hex`와 `expected_hex`를 그냥 비교하지 않고 `constant_time_compare`에 태운 것도 의미가 있다. 여기서 timing safety 자체가 중요한 보안 구현은 아니지만, "비밀값 비교는 별도 primitive가 필요하다"는 메시지를 evaluator 레벨에서도 흘리지 않게 된다.

새로 배운 것:

- reference vector는 정답 표가 아니라 입력 contract를 고정하는 장치다.
- 특히 HKDF manifest가 RFC 5869 case 1을 `encoding: "hex"`로 남기는 방식은, primitive 설명을 문장보다 fixture가 더 정확하게 붙드는 예시였다.

다음:

- 이제 남은 질문은 primitive 결과를 한 번 더 사람이 읽을 수 있는 demo로 어떻게 묶을 것인가였다.

## Day 2
### Session 1

- 당시 목표: vector pass/fail만으로 끝내지 않고 hash, MAC, KDF 차이를 한 번에 보이는 deterministic demo를 만든다.
- 변경 단위: `python/src/crypto_primitives_in_practice/vectors.py`의 `demo_from_profile`, `python/src/crypto_primitives_in_practice/cli.py`, `python/tests/test_cli.py`
- 처음 가설: demo는 각 primitive 출력만 나열하면 충분할 것 같았다.
- 실제 진행: 비교 포인트가 없는 hex dump는 설명력이 약해서, `hash_equals_mac`와 `mac_self_check`를 같이 넣고 HKDF는 base64url까지 만들어 token-ish 출력을 보여 주도록 바꿨다.

CLI:

```bash
$ PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
    .venv/bin/python -m pytest study/01-crypto-primitives-in-practice/python/tests
..........                                                               [100%]
10 passed in 0.06s
```

```bash
$ PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
    .venv/bin/python -m crypto_primitives_in_practice.cli demo \
    study/01-crypto-primitives-in-practice/problem/data/demo_profile.json
{
  "profile": "auth-token-ish-demo",
  "hash": {"sha256_hex": "4f57d7ae81a37083d36a9385395a31b0659036d27d52b08f7940cdd96ecc5c48"},
  "mac": {"hmac_sha256_hex": "68a76d599c23e7cbe38f05392bc0b8e0498caeef9562be7a7755396b5bbda01d"},
  "comparisons": {"hash_equals_mac": false, "mac_self_check": true}
}
```

검증 신호:

- CLI 테스트는 `check-vectors`와 `demo` 둘 다 deterministic output을 기대값 그대로 확인한다.
- demo 결과에서 같은 message를 써도 hash와 MAC은 다르고, 같은 key와 message로 다시 계산한 MAC만 self check를 통과한다.

핵심 코드:

```python
def demo_from_profile(path: Path) -> dict[str, Any]:
    profile = load_json(path)
    encoding = str(profile.get("encoding", "utf-8"))
    message = _decode(str(profile["message"]), encoding)
    secret = _decode(str(profile["shared_secret"]), encoding)
    password = _decode(str(profile["password"]), encoding)
```

왜 이 코드가 중요했는가:

demo profile은 한 primitive만 설명하지 않는다. 같은 profile에서 공개 message, shared secret, password, ikm을 따로 꺼내기 때문에 "입력 종류가 다르면 같은 보안 함수라고 부르면 안 된다"는 사실을 한 번에 다시 보여 준다.

결정적인 장면은 마지막 출력 포맷이다.

```python
        "kdf": {
            "pbkdf2_hmac_sha1_hex": pbkdf2_hex,
            "hkdf_sha256_hex": hkdf_hex,
            "hkdf_sha256_base64url": base64.urlsafe_b64encode(bytes.fromhex(hkdf_hex))
            .rstrip(b"=")
            .decode(),
        },
        "comparisons": {
            "hash_equals_mac": constant_time_compare(digest_hex, mac_hex),
            "mac_self_check": constant_time_compare(mac_hex, hmac_sha256(secret, message)),
        },
```

`hash_equals_mac`를 일부러 노출한 건 "둘 다 hex니까 비슷하다"는 착시를 깨기 위해서다. 반대로 `hkdf_sha256_base64url`은 HKDF가 실제 token material처럼 어디에 쓰일 수 있는지 보여 준다. 이 프로젝트는 학술 설명보다 실행 가능한 비교점을 남기는 쪽을 택한다.

새로 배운 것:

- deterministic demo는 test보다 친절하지만, test만큼 엄격해야 의미가 있다.
- `test_hmac_changes_when_key_changes`, `test_pbkdf2_changes_when_iterations_change`, `test_hkdf_changes_when_info_changes`가 같이 있어야 demo가 단순 예시 출력으로 무너지지 않는다.

다음:

- 범위를 더 넓힌다면 Argon2id, scrypt, AEAD처럼 지금 빠진 primitive를 넣는 대신, 같은 "입력 경계" 원칙으로 어디까지 확장할지부터 다시 정해야 한다.
