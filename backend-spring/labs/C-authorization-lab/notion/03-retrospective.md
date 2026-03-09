# Retrospective

## What improved

- authorization을 auth와 분리해 보는 순서가 맞았다.
- invite lifecycle을 넣은 덕분에 단순 role toggle보다 현실적인 membership model이 보였다.
- ownership과 membership를 나눠 생각하는 연습이 생겼다.

## What is still weak

- in-memory state는 persistence 문제를 가린다.
- Spring method security로 넘어가는 다리가 아직 약하다.
- richer denial-path coverage가 부족하다.

## What to revisit

- membership persistence를 PostgreSQL로 옮길 수 있다.
- `@PreAuthorize` 같은 method security로 재구성할 수 있다.
- FastAPI authorization lab과 enforcement 위치를 비교할 수 있다.

