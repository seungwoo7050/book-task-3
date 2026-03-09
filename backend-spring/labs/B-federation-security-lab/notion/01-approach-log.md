# Approach Log

## Options considered

- Google OAuth만 두고 2FA를 빼는 방식은 단순하지만 session hardening이 약해진다.
- 2FA만 별도 랩으로 떼는 방식은 auth story가 너무 조각난다.
- fully real provider integration은 의미 있지만 scaffold 단계에서는 환경 의존성이 크다.

## Chosen direction

- package structure:
  - federation과 2FA를 한 workspace에 둔다
- persistence choice:
  - initial scaffold는 audit와 external linking 방향성을 먼저 보여 준다
- security boundary:
  - provider callback 이후에도 second factor와 throttling이 남는다
- integration style:
  - simulated provider contract를 유지한다
- why this is the right choice:
  - Spring auth story에서 “higher assurance session”을 한 랩으로 설명하기 좋다

## Rejected ideas

- live Google console 연동을 랩 필수 조건으로 두는 방식은 폐기했다
- audit logging을 빼는 방식은 폐기했다. security lab의 운영 관점이 약해진다

## Evidence

- `/Users/woopinbell/work/web-pong/study2/labs/B-federation-security-lab/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/labs/B-federation-security-lab/docs/README.md`

