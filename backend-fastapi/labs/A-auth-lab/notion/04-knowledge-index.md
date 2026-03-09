# Knowledge Index

## 이 랩에서 체득한 핵심 개념들

### Argon2 password hashing

비밀번호를 평문으로 저장하면 안 된다는 건 누구나 안다. 하지만 "왜 bcrypt 대신 Argon2인가?"라는 질문에 답하려면 조금 더 깊이 들어가야 한다.

Argon2는 memory-hard 해시 함수다. 즉, GPU 병렬 공격에 대한 비용을 의도적으로 높인다. 이 랩에서는 `argon2-cffi` 라이브러리의 `PasswordHasher`를 사용했고, `hash_password()`와 `verify_password()` 두 함수로 래핑해서 서비스 전체에서 일관되게 썼다. 해시 실패 시 `VerifyMismatchError`와 `InvalidHashError`를 잡아서 False를 반환하는 방식으로, 타이밍 공격 면에서도 안전한 패턴을 유지했다.

### Refresh-token rotation

access token은 짧게(15분), refresh token은 길게(14일) 발행한다. 문제는 refresh token이 탈취되면 공격자가 오래 세션을 유지할 수 있다는 것이다. 이를 막기 위해 **rotation**을 도입했다: refresh token을 한 번 사용하면 즉시 폐기하고, 새 refresh token을 발행한다.

여기서 한 발 더 나아간 것이 **family-based reuse detection**이다. 같은 family_id를 가진 토큰 중 이미 revoke된 토큰이 다시 사용되면, 해당 family 전체를 일괄 revoke한다. 이렇게 하면 공격자가 탈취한 토큰을 쓰는 순간, 정상 사용자의 세션도 끊기면서 "뭔가 잘못되었다"는 신호를 만들어낸다.

### Cookie + CSRF pairing

HttpOnly cookie로 토큰을 전달하면 JavaScript에서 접근할 수 없어 XSS에 강하다. 하지만 cookie는 브라우저가 자동으로 붙이기 때문에 CSRF 공격에는 취약하다. 이 랩에서는 CSRF token을 별도의 non-HttpOnly cookie로 내보내고, 클라이언트가 이 값을 `X-CSRF-Token` 헤더로 함께 보내도록 요구했다. 서버는 `secrets.compare_digest()`로 cookie 값과 header 값을 비교해서, 둘이 일치할 때만 요청을 수락한다.

## 용어 정리

- **verification token**: 이메일 소유를 증명하기 위한 일회성 토큰. 이 랩에서는 `secrets.token_urlsafe(32)`로 생성하고, HMAC-SHA256으로 해시한 값을 DB에 저장한다.
- **reset token**: 비밀번호 변경 권한을 한시적으로 위임하는 토큰. verification token과 생성 방식은 같지만, TTL이 30분으로 훨씬 짧다.
- **token family**: 같은 로그인 세션에서 파생된 refresh token들의 그룹. family_id로 묶여 있어서, 하나가 재사용되면 전체를 revoke할 수 있다.

## 참고한 자료

- `fastapi/README.md`: 실행 명령과 범위를 맞추기 위해 확인. 이 랩은 로컬 auth에 집중하고 OAuth/2FA를 의도적으로 제외한다는 점을 재확인했다.
- FastAPI 공식 문서의 Security 섹션: cookie 기반 인증과 dependency injection 패턴 참고.
- Argon2 RFC (RFC 9106): memory-hard hashing의 이론적 배경 참고.
