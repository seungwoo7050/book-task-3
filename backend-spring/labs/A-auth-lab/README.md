# A-auth-lab

로컬 계정 인증 백엔드에서 어디까지를 "기본 인증 흐름"으로 설명해야 하는지 정리하는 랩입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- 사용자는 회원가입하고 로그인하고, 세션을 갱신하고, 필요하면 계정을 복구할 수 있어야 합니다.
- frontend 없이도 refresh rotation, cookie, CSRF 같은 인증 경계를 설명할 수 있어야 합니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- 단일 Spring 워크스페이스에서 register, login, refresh, logout, `me` 흐름을 구현했습니다.
- Mailpit 기반 로컬 메일 흐름을 염두에 두고 이메일 검증과 비밀번호 재설정 개념을 문서와 API shape로 정리했습니다.
- refresh token rotation과 cookie + CSRF 경계를 한 랩 안에서 같이 설명할 수 있게 만들었습니다.

## 핵심 설계 선택

- OAuth, 2FA는 이 랩에 섞지 않고 다음 단계인 [B-federation-security-lab](../B-federation-security-lab/README.md)로 넘겼습니다.
- persistence보다 인증 흐름의 shape를 먼저 이해하도록 초기 scaffold 성격을 유지했습니다.
- Mailpit-ready 환경을 문서화해 외부 SMTP 없이도 로컬에서 흐름을 재현할 수 있게 했습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- 실제 Google OAuth 같은 외부 로그인
- production-grade 사용자 persistence
- 브라우저 기반 cookie 동작 전체 검증

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
