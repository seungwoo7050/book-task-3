# Retrospective

## What improved

- local auth 다음 단계로 어떤 보안 주제를 봐야 하는지 순서가 분명해졌다.
- federation과 2FA를 같이 묶은 설계가 auth hardening 맥락을 잘 살렸다.
- audit logging을 같은 랩에 넣은 점이 실무 감각을 높였다.

## What is still weak

- Google integration은 여전히 mocked contract다.
- TOTP hardness는 학습 친화적으로 단순화되어 있다.
- hard rate limiting은 fully enforced behavior가 아니다.

## What to revisit

- Spring Security OAuth2 client와 실제 provider config를 붙여 볼 수 있다.
- Redis-backed limiter를 실제로 강제하는 실험을 추가할 수 있다.
- capstone과 연결해 external identity persistence를 비교할 수 있다.

