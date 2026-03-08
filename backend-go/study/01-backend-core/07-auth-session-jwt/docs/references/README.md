# References

## 1. OWASP Password Storage Cheat Sheet

- Title: Password Storage Cheat Sheet
- URL: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Checked date: 2026-03-07
- Why: password hashing 기본 원칙을 다시 확인했다.
- Learned: 입문 예제라도 해시 저장을 기본으로 두는 편이 좋다.
- Effect: bcrypt를 최소 외부 의존성으로 채택했다.

## 2. JSON Web Token

- Title: RFC 7519 JSON Web Token (JWT)
- URL: https://www.rfc-editor.org/rfc/rfc7519
- Checked date: 2026-03-07
- Why: JWT claims와 만료 필드 의미를 다시 확인했다.
- Learned: 예제에서는 최소 claims만 두는 편이 개념 전달에 낫다.
- Effect: `sub`, `role`, `exp`만 사용했다.

