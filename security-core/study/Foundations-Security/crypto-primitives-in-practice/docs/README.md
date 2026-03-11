# 문서 묶음 안내

이 문서 묶음은 “암호학 함수를 호출했다”가 아니라 “왜 이 primitive를 골랐는가”를 설명하기 위한 개념 지도입니다.

## 먼저 보면 좋은 질문

- hash, MAC, KDF는 각각 무엇을 증명하거나 보호하는가
- password KDF와 key expansion KDF는 왜 같은 KDF가 아닌가
- plain hash는 왜 인증이나 메시지 무결성을 대신하지 못하는가

## 읽고 나면 설명할 수 있어야 하는 것

- secret input과 public input의 차이
- SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1의 역할 분리
- reference vector가 왜 이 프로젝트의 가장 중요한 검증 근거인가

## 함께 보면 좋은 문서

1. [concepts/hash-vs-mac-vs-kdf.md](concepts/hash-vs-mac-vs-kdf.md)
2. [references/README.md](references/README.md)
3. [공용 가이드](../../../../../guides/security/crypto-primitives.md)
