# 참고 자료

이 프로젝트는 구현 범위를 일부러 작게 잡고, 각 primitive를 reference vector로 재현하는 데 집중합니다.

## 핵심 출처

- RFC 5869: HKDF test case 1의 입력과 기대 출력
- RFC 6070: PBKDF2-HMAC-SHA1 test case 1, 2의 입력과 기대 출력
- NIST / FIPS SHA-256 설명 자료: digest의 역할과 충돌/무결성 기본 개념
- OWASP Password Storage Cheat Sheet: production password KDF 선택 시 PBKDF2와 Argon2id의 차이

## 이 문서가 하는 일

- vector provenance를 남깁니다.
- 지금 구현이 reference reproduction인지, production 설계 추천안인지 구분합니다.
- 후속 프로젝트에서 무엇을 더 다뤄야 하는지 경계를 남깁니다.

