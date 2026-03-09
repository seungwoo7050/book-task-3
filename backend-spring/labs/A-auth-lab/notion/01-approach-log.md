# Approach Log

## Options considered

- 처음부터 persisted user table과 full reset flow까지 넣는 방식은 현실적이지만, 첫 Spring 랩으로는 무겁다.
- contract-first scaffold는 얕아질 위험이 있지만, Spring auth 용어와 경계를 빠르게 고정하기 좋다.
- cookie를 실제 response cookie로 다루는 방식은 중요하지만, 초기 scaffold에서는 API shape 설명이 먼저였다.

## Chosen direction

- package structure:
  - auth 중심 단일 Spring workspace
- persistence choice:
  - initial scaffold에서는 lightweight persistence와 modeled flow를 허용한다
- security boundary:
  - refresh rotation과 cookie/CSRF pairing을 먼저 드러낸다
- integration style:
  - Mailpit-ready local stack을 두되 full mail lifecycle은 뒤로 미룬다
- why this is the right choice:
  - 첫 Spring 랩에서 개념 지형도를 잡기에 적당하다

## Rejected ideas

- OAuth와 2FA를 함께 넣는 방식은 폐기했다. A랩의 범위를 흐린다.
- full browser-integrated cookie behavior를 첫 랩 필수로 두는 방식은 폐기했다. 학습 반복 속도가 느려진다.

## Evidence

- `/Users/woopinbell/work/web-pong/study2/labs/A-auth-lab/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/labs/A-auth-lab/docs/README.md`
- `make test`

