# A-auth-lab

로컬 계정 인증 백엔드에서 어디까지를 "기본 인증 흐름"으로 설명해야 하는지 정리하는 랩입니다. 로그인 한 번만 만드는 것이 아니라, 이메일 검증, 비밀번호 재설정, refresh token rotation, cookie + CSRF 보호까지 한 묶음으로 다룹니다.

## 문제 요약

- 사용자는 회원가입하고, 이메일을 검증하고, 로그인하고, 필요하면 비밀번호를 재설정할 수 있어야 합니다.
- 인증이 끝난 뒤에도 세션 유지와 상태 변경 요청 보호를 함께 설명할 수 있어야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- 단일 FastAPI 워크스페이스에서 회원가입, 로그인, 로그아웃, 이메일 검증, 비밀번호 재설정, refresh token rotation을 구현했습니다.
- 비밀번호는 Argon2로 해시하고, cookie 기반 인증 요청에는 CSRF 검증을 함께 붙였습니다.
- 로컬 메일 검증 실험은 Mailpit을 기준으로 정리해 외부 SMTP 없이도 흐름을 재현할 수 있게 했습니다.

## 핵심 설계 선택

- access token과 refresh token의 책임을 나눠 세션 갱신과 탈취 위험 설명을 분리했습니다.
- 이메일 검증과 비밀번호 재설정을 모두 "토큰 발급/소비" 문제로 보되, 사용 목적과 만료 조건은 구분했습니다.
- OAuth와 2FA는 이 랩에 섞지 않고 다음 단계인 [B-federation-security-lab](../B-federation-security-lab/README.md)로 넘겼습니다.

## 검증

```bash
cd fastapi
make lint
make test
make smoke
docker compose up --build
```

- 실행과 환경 설명은 [fastapi/README.md](fastapi/README.md)에서 다룹니다.
- 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 제외 범위

- Google OAuth 같은 외부 로그인
- TOTP 2FA와 recovery code
- 운영용 메일 인프라와 실제 외부 SMTP 검증

## 다음 랩

- 다음 단계는 [B-federation-security-lab](../B-federation-security-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
