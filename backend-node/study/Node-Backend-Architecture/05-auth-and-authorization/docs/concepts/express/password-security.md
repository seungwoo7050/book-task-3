# bcrypt과 비밀번호 보안

## 왜 비밀번호를 해싱해야 하는가?

비밀번호를 평문으로 저장하면 데이터베이스가 유출되었을 때 모든 사용자의 비밀번호가 노출된다. 해싱은 **일방향 함수**로, 원본 비밀번호를 복원할 수 없다.

```
평문: "mypassword123"
해시: "$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy"
```

## bcrypt의 동작 원리

bcrypt는 **적응형 해시 함수**이다. 핵심 특성:

1. **Salt 자동 생성**: 매번 다른 랜덤 salt를 사용하여 동일한 비밀번호도 다른 해시를 생성
2. **Cost Factor (Salt Rounds)**: 연산량을 조절하여 brute-force 공격을 어렵게 함

```typescript
import bcrypt from "bcryptjs";

// 해싱 (Salt Rounds = 10)
const hashed = await bcrypt.hash("mypassword", 10);

// 검증
const isValid = await bcrypt.compare("mypassword", hashed); // true
const isWrong = await bcrypt.compare("wrongpass", hashed);   // false
```

### Salt Rounds 선택 가이드

| Rounds | 대략적 시간 | 용도 |
|--------|------------|------|
| 8 | ~40ms | 개발/테스트 |
| 10 | ~100ms | 일반 웹 앱 (이 과제의 선택) |
| 12 | ~300ms | 높은 보안이 필요한 경우 |
| 14+ | ~1s+ | 매우 민감한 시스템 |

이 과제에서는 salt rounds 10을 사용한다:
```typescript
const hashedPassword = await bcrypt.hash(dto.password, 10);
```

## bcrypt vs bcryptjs

| 패키지 | 특성 |
|--------|------|
| `bcrypt` | C++ 네이티브 바인딩, 더 빠르지만 빌드 도구 필요 |
| `bcryptjs` | 순수 JavaScript, 빌드 도구 불필요, 약간 느림 |

이 과제에서는 설치 편의성을 위해 `bcryptjs`를 사용한다.

## 인증 흐름에서의 bcrypt

```
[회원가입]
  client → { username: "john", password: "abc123" }
  server → bcrypt.hash("abc123", 10) → "$2a$10$..."
  server → Map에 저장: { password: "$2a$10$..." }

[로그인]
  client → { username: "john", password: "abc123" }
  server → Map에서 user 조회
  server → bcrypt.compare("abc123", user.password) → true
  server → jwt.sign(payload) → token 발급
```

## 참고 자료

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [bcryptjs npm](https://www.npmjs.com/package/bcryptjs)

## 근거 요약

- 근거: [문서] `backend-architecture/02-auth-guards/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/lab-report.md`
- 근거: [문서] `backend-architecture/02-auth-guards/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/express-impl/devlog/README.md`
