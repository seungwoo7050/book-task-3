# B-federation-security-lab series map

local auth 다음에 붙는 federation, 2FA, audit를 어떤 순서로 분리했는지 보여 주는 시리즈다. 기준 환경은 macOS + VSCode 통합 터미널이다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md): authorize URL, callback, TOTP, audit가 어떻게 하나의 인증 강화 랩으로 묶였는지 따라간다.

## 이 시리즈가 답하는 질문

- 왜 live Google 연동보다 callback contract를 먼저 고정했는가
- TOTP와 audit를 왜 같은 랩에서 다뤘는가
- 무엇을 증명했고 무엇을 다음 단계로 남겼는가
