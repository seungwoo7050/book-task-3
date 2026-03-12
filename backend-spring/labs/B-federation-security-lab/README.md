# B-federation-security-lab

로컬 계정 인증 이후에 OAuth2 federation, 2FA, audit를 어떻게 보강할지 정리하는 랩입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- 로컬 로그인만으로는 설명되지 않는 외부 identity 연동과 두 번째 인증 수단이 필요합니다.
- 하지만 실제 provider 연동을 붙이기 전에, 어떤 경계와 실패 지점을 설명해야 하는지 먼저 분리할 필요가 있습니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- Google OAuth2 authorize/callback 형태를 흉내 낸 federation flow를 구현했습니다.
- TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다뤘습니다.
- audit log surface를 추가해 로그인 강화 기능이 남기는 흔적까지 함께 설명할 수 있게 했습니다.

## 핵심 설계 선택

- 실제 Google Console 연동 대신 callback contract를 먼저 모델링해 문제를 작게 쪼갰습니다.
- 2FA와 audit를 federation과 함께 묶어 "인증 강화"라는 하나의 주제로 읽히게 했습니다.
- rate limiting은 구현 과시보다 문제 인식에 집중하고, enforcement는 다음 단계로 남겼습니다.

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

- 실제 Google OAuth provider integration
- production-grade TOTP secret 관리
- Redis-backed hard rate limit enforcement

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
