# Approach Log

## Options considered

- Spring Security method annotations를 바로 쓰는 방식은 좋지만, 첫 scaffold에서는 rule 자체가 보이지 않을 수 있다.
- service logic 중심 접근은 단순하지만, annotation 기반 정책으로 확장할 여지가 남는다.
- membership를 DB에 바로 넣는 방식은 현실적이지만, 초기 반복 속도가 느려진다.

## Chosen direction

- package structure:
  - invite, membership, role decision 중심
- persistence choice:
  - initial scaffold는 in-memory state를 허용
- security boundary:
  - auth보다 permission decision을 먼저 강조
- integration style:
  - API shape와 service logic에서 ownership/rbac를 드러냄
- why this is the right choice:
  - authorization problem을 가장 작은 형태로 분리해 볼 수 있다

## Rejected ideas

- full auth integration은 폐기했다. 실패 원인이 섞인다.
- policy engine 도입은 폐기했다. 랩 범위를 넘는다.

## Evidence

- `/Users/woopinbell/work/web-pong/study2/labs/C-authorization-lab/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/labs/C-authorization-lab/docs/README.md`

