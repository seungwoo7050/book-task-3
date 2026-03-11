# 접근 로그

## 선택한 방향

- stdlib-first: crypto 라이브러리 래퍼보다 입력/출력 경계를 먼저 이해하는 것이 목적이므로 `hashlib`, `hmac`만 사용했습니다.
- vector-first: 설명보다 검증 근거가 먼저 보이도록 CLI를 `check-vectors` 중심으로 뒀습니다.
- split vocabulary: password KDF와 key expansion KDF를 같은 API 설명으로 뭉개지 않도록 PBKDF2와 HKDF를 함께 두었습니다.

## 버린 방향

- Argon2id까지 한 번에 넣는 방향은 production recommendation과 reference vector 재현 목표가 섞여서 범위를 흐릴 수 있어 제외했습니다.
- JWT/OAuth demo를 함께 넣는 방향은 primitive 구분보다 응용 계층 설명이 더 커져서 제외했습니다.

