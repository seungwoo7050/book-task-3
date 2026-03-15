# security-core 서버 개발 비필수 문제지

여기서 `elective`는 서버 공통 필수보다 보안 원리 이해 쪽 비중이 더 큰 문제라는 뜻입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-crypto-primitives-in-practice-python](01-crypto-primitives-in-practice-python.md) | 시작 위치의 구현을 완성해 SHA-256, HMAC-SHA256, HKDF-SHA256, PBKDF2-HMAC-SHA1 vector가 모두 통과해야 합니다, check-vectors <manifest>가 primitive별 결과를 JSON으로 출력해야 합니다, demo <profile>가 hash, MAC, KDF 결과를 deterministic하게 출력해야 합니다를 한 흐름으로 설명하고 검증한다. | `make test-unit && make demo-crypto` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
