# Primitive를 나누고, vector로 고정하고, demo로 끝맺기까지

`security-core`의 첫 프로젝트는 알고리즘 수를 늘리는 데서 출발하지 않는다. 먼저 더 기본적인 질문부터 정리해야 했다. `hash`, `MAC`, `KDF`를 한 문단에 묶어 두면, 나중에 CLI를 붙여도 왜 입력이 다르고 왜 목적이 다른지 다시 흐려진다. 그래서 이 프로젝트는 primitive surface를 먼저 갈라 놓고, 그다음 reference vector로 경계를 고정한 뒤, 마지막에 demo CLI로 사람이 읽는 표면까지 닫는 순서로 만들어졌다.

## 구현 순서 요약

- `primitives.py`에서 SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1을 서로 다른 입력 규칙을 가진 함수로 분리했다.
- `vectors.py`에서 manifest decoding, primitive dispatch, `actual_hex`와 `expected_hex` 비교를 한 summary로 묶었다.
- `cli.py`와 `test_cli.py`에서 `check-vectors`, `demo` JSON 계약을 고정해 primitive 차이를 사람이 읽는 출력으로 마무리했다.

## Session 1

첫 장면은 README가 아니라 `primitives.py`였다. 이 프로젝트에서 가장 먼저 고정해야 할 것은 설명 문체가 아니라 함수 경계였기 때문이다. `sha256_digest()`는 공개 입력을 digest로 압축하는 함수고, `hmac_sha256()`은 secret key와 message를 함께 받아 인증 가능한 출력을 만든다. 둘 다 hex 문자열을 돌려주지만, 같은 질문에 답하는 함수는 아니다. 이 차이를 코드 표면에서 먼저 분리해 두지 않으면 이후의 vector와 demo도 모두 모호해진다.

가장 중요한 전환점은 HKDF와 비교 함수였다.

```python
def hkdf_sha256(ikm: bytes, salt: bytes, info: bytes, length: int) -> str:
    if length <= 0:
        raise ValueError("length must be positive")
    if length > 255 * hashlib.sha256().digest_size:
        raise ValueError("length exceeds HKDF-SHA256 limit")

    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    okm = bytearray()
    previous_block = b""
    counter = 1

    while len(okm) < length:
        previous_block = hmac.new(
            prk,
            previous_block + info + bytes([counter]),
            hashlib.sha256,
        ).digest()
        okm.extend(previous_block)
        counter += 1

    return bytes(okm[:length]).hex()
```

이 loop를 보는 순간 HKDF를 더 이상 “hash를 한 번 더 하는 함수”처럼 설명하기 어렵다. 이미 secret인 key material에서 context별 하위 키를 뽑아내는 쪽이기 때문이다. 같은 KDF라는 말 아래에 PBKDF2와 HKDF를 묶어 둘 수는 있어도, 하나는 password hardening이고 다른 하나는 key expansion이라는 차이는 여기서 분명해진다.

```python
def constant_time_compare(left: str, right: str) -> bool:
    return compare_digest(left, right)
```

`compare_digest()`를 따로 감싼 것도 같은 맥락이었다. MAC이나 token 비교는 “문자열이 같은가”만 보는 작업이 아니라, timing signal을 새지 않고 같은지 확인하는 작업이다. 나중에 `vectors.py`와 `demo_from_profile()`이 이 함수를 재사용하면서, 비교 방식 자체도 primitive surface의 일부라는 점이 더 분명해졌다.

이 시점에 다시 돌린 검증은 전체 패키지 테스트였다.

```bash
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m pytest study/01-crypto-primitives-in-practice/python/tests
```

검증 신호는 단순하지만 충분히 강했다.

- `10 passed in 0.06s`
- primitive 함수, manifest 처리, CLI output shape가 한 번에 통과했다.

여기서 처음 또렷해진 개념은 `hash != MAC != KDF`라는 말을 추상 구호가 아니라 입력 성격으로 설명해야 한다는 점이었다. `hash`는 공개 입력도 받을 수 있고, `MAC`은 secret을 알고 있다는 사실을 증명하며, `KDF`는 secret 재료를 다른 목적의 key material로 바꾼다. 출력 형식이 비슷해 보여도 질문은 완전히 다르다.

## Session 2

primitive 함수를 분리했다고 설명이 끝나지는 않았다. 함수 경계를 코드에 새겼다면, 그다음에는 그 경계가 실제로 무엇을 계산하는지 고정해야 했다. 그래서 두 번째 세션의 중심은 `vectors.py`였다. 여기서는 알고리즘 구현보다 manifest를 읽는 계약이 훨씬 중요했다.

```python
def _compute_actual_hex(primitive: str, manifest: dict[str, Any], vector: dict[str, Any]) -> str:
    encoding = _encoding(manifest, vector)

    if primitive == "sha256":
        return sha256_digest(_decode(str(vector["message"]), encoding))
    if primitive == "hmac-sha256":
        return hmac_sha256(
            _decode(str(vector["key"]), encoding),
            _decode(str(vector["message"]), encoding),
        )
    if primitive == "hkdf-sha256":
        return hkdf_sha256(
            _decode(str(vector["ikm"]), encoding),
            _decode(str(vector["salt"]), encoding),
            _decode(str(vector["info"]), encoding),
            int(vector["length"]),
        )
```

이 dispatch가 중요한 이유는 모든 fixture를 같은 JSON 껍데기로 읽으면서도 primitive마다 전혀 다른 입력 규칙을 유지하기 때문이다. hash는 `message`만 있으면 되지만, HMAC은 `key + message`, HKDF는 `ikm + salt + info + length`, PBKDF2는 `password + salt + iterations + length`가 필요하다. `_decode()`와 `_encoding()`이 끼어들어 주지 않으면, 같은 manifest format으로 서로 다른 입력 경계를 설명하기 어렵다.

summary는 더 짧지만 이 프로젝트의 핵심 계약은 오히려 여기에 더 선명하게 담긴다.

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

`matched`를 `constant_time_compare()`로 두면서, 이 프로젝트는 “계산이 맞다”와 “비밀값 비교 규칙이 다르다”를 같은 surface에 남긴다. reference vector가 단순한 테스트 부속물이 아니라 primitive 설명의 본체가 되는 장면이 바로 여기다.

이 단계에서 가장 직접적인 CLI는 HKDF vector였다.

```bash
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli check-vectors \
  study/01-crypto-primitives-in-practice/problem/data/hkdf_sha256_vectors.json
```

판단을 바꾼 출력은 이 값들이었다.

- `manifest`: `hkdf_sha256_vectors.json`
- `primitive`: `hkdf-sha256`
- `passed`: `1`
- `failed`: `0`
- `results[0].name`: `rfc-5869-case-1`
- `matched`: `true`

여기서 새로 배운 것은 reference vector의 역할이었다. vector는 구현이 RFC와 맞는지 확인하는 도구일 뿐 아니라, “이 입력 모양을 이 primitive가 책임진다”는 경계를 문서보다 더 단단하게 고정한다.

## Session 3

vector가 통과했다고 곧바로 학습 surface가 닫히는 것은 아니었다. 이 프로젝트가 정말 읽히려면, 사람에게 “왜 hash와 MAC을 갈라 놓았는가”를 한 번 더 납득시키는 demo가 필요했다. 그래서 마지막에는 `demo_from_profile()`과 CLI output shape를 다듬는 쪽으로 갔다.

```python
return {
    "profile": str(profile["profile"]),
    "hash": {
        "sha256_hex": digest_hex,
    },
    "mac": {
        "hmac_sha256_hex": mac_hex,
    },
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
}
```

특히 `comparisons` 블록이 중요했다. 이 부분이 없었다면 demo는 긴 hex dump로 끝났을 것이다. 그런데 `hash_equals_mac`과 `mac_self_check`가 들어가자, 같은 입력을 써도 hash는 인증을 대신하지 못하고, HMAC만이 shared secret을 아는 쪽이 만들었다는 사실을 보여 준다는 점이 훨씬 쉽게 읽힌다.

CLI surface는 이렇게 닫혔다.

```bash
PYTHONPATH=study/01-crypto-primitives-in-practice/python/src \
  .venv/bin/python -m crypto_primitives_in_practice.cli demo \
  study/01-crypto-primitives-in-practice/problem/data/demo_profile.json
```

이 출력에서 남겨 둘 신호는 추상 요약이 아니라 구체적인 비교 포인트였다.

- `profile`: `auth-token-ish-demo`
- `hash.sha256_hex`: `4f57d7ae81a37083...`
- `mac.hmac_sha256_hex`: `68a76d599c23e7cb...`
- `kdf.hkdf_sha256_base64url`: `HHaXak39_du2wEmxB0NidhO2XSg_aXtWM7tpSKjYlHQ`
- `comparisons.hash_equals_mac`: `false`
- `comparisons.mac_self_check`: `true`

마지막에 `test_cli.py`가 고정한 것도 바로 이 shape였다. `check-vectors`는 manifest summary를, `demo`는 사람이 읽는 비교 surface를 돌려주도록 역할을 나눴다. 그 덕분에 이 프로젝트는 “primitive 설명문”이 아니라 “primitive 경계를 코드와 CLI로 재현하는 랩”으로 마감됐다.

## 다음

여기서 얻은 것은 crypto primitive 몇 개를 돌리는 방법만이 아니었다. 서로 다른 보안 질문을 서로 다른 vocabulary로 말해야 한다는 감각이었다. 다음 프로젝트 `auth-threat-modeling`은 그 감각을 함수 경계가 아니라 control gap과 finding ID 쪽으로 밀어붙인다.
