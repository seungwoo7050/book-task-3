# A-auth-lab series map

로컬 계정 인증을 어디까지 baseline auth로 볼지 빠르게 파악하게 해 주는 시리즈다. macOS에서 VSCode로 `spring/` 워크스페이스를 열고 통합 터미널에서 검증하는 흐름을 기준으로 읽으면 된다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md): register, login, refresh rotation, CSRF 경계가 어떤 순서로 굳어졌는지 따라간다.

## 이 시리즈가 답하는 질문

- 왜 OAuth나 2FA를 이 랩에 넣지 않았는가
- refresh rotation을 왜 baseline auth에 포함했는가
- persistence를 얕게 둔 상태에서 무엇까지 검증했는가
