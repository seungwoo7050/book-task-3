# security-core 서버 개발 비필수 답안지

이 문서는 crypto primitive 과제를 실제 source와 테스트만으로 해설하는 답안지다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-crypto-primitives-in-practice-python](01-crypto-primitives-in-practice-python_answer.md) | 시작 위치의 구현을 완성해 SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector가 모두 통과해야 합니다, check-vectors <manifest>가 primitive별 결과를 JSON으로 출력해야 합니다, demo <profile>가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 check_vectors와 demo, sha256_digest 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test-unit && make demo-crypto` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
