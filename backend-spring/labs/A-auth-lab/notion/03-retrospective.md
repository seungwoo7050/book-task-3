# Retrospective

## What improved

- Spring auth 학습의 첫 단계를 너무 무겁지 않게 시작할 수 있게 되었다.
- cookie, CSRF, refresh rotation 같은 용어를 초반부터 고정한 판단이 좋았다.
- Mailpit-ready local stack 덕분에 backend-only 학습 흐름이 자연스러워졌다.

## What is still weak

- user, verification token, refresh family persistence가 아직 얕다.
- reset와 verify는 API-first 설명이 더 강하다.
- Spring Security의 deeper integration은 아직 capstone 전 단계다.

## What to revisit

- cookie를 실제 브라우저/response semantics로 더 엄격히 다룰 수 있다.
- PostgreSQL persistence를 더 일찍 넣을지 다시 검토할 수 있다.
- FastAPI A랩과 개념 비교표를 만들 수 있다.

