# B-federation-security-lab structure outline

## 글 목표

- federation, 2FA, audit가 왜 같은 랩으로 묶였는지 구현 순서로 보여 준다.
- macOS + VSCode 통합 터미널 기준의 실행 흐름을 유지한다.

## 글 순서

1. live provider 대신 callback contract를 먼저 고정한 단계
2. TOTP와 audit를 한 흐름으로 묶은 단계
3. production concern을 어디까지 남겼는지 닫는 단계

## 반드시 넣을 코드 앵커

- `FederationSecurityApiTest.googleCallbackAndAuditFlowWork()`
- `FederationSecurityDemoService.authorize()`
- `FederationSecurityDemoService.setupTotp()`

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- federation의 핵심은 provider SDK보다 callback contract다.
- 2FA는 audit까지 포함한 상태 변화로 봐야 한다.
