# Approach Log

## Options considered

- 처음부터 포트폴리오-grade capstone으로 바로 가는 방식은 좋지만, baseline 비교 지점이 사라진다.
- scaffold capstone을 별도로 보존하는 방식은 중복이 생기지만 학습 이력 보존에 유리하다.
- 커머스 도메인은 auth, catalog, order, notification을 한 서비스 안에 묶기 좋아 baseline domain으로 적당하다.

## Chosen direction

- package structure:
  - 모듈형 모놀리스 형태의 commerce service
- persistence choice:
  - core concept는 relational model과 local stack으로 시작
- security boundary:
  - auth surface는 존재하지만 full depth는 이후 개선 대상으로 남김
- integration style:
  - catalog/cart/order와 async hook을 한 도메인에 모음
- why this is the right choice:
  - Spring track의 capstone baseline으로 쓰기 좋다

## Rejected ideas

- lab 코드를 그대로 import하는 방식은 폐기했다
- 포트폴리오 최종본으로 바로 주장하는 방식은 폐기했다

## Evidence

- `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend/docs/README.md`
- `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/README.md`

