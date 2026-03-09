# Retrospective

## What improved

- Spring track에 통합 도메인 기준점이 생겼다.
- 커머스 도메인을 택한 덕분에 auth, catalog, order, notification을 자연스럽게 연결할 수 있었다.
- baseline이 남아 있어서 v2 개선의 이유를 설명하기 쉬워졌다.

## What is still weak

- auth 깊이가 얕다.
- payment가 없다.
- async consumer/runtime integration이 충분히 완성되어 있지 않다.

## What to revisit

- baseline과 v2의 차이를 별도 비교 문서로 적을 수 있다.
- 각 모듈을 persisted flow로 얼마나 끌어올릴지 기준을 더 분명히 둘 수 있다.
- portfolio-grade 프로젝트로 쓸 경우에는 v2만 전면에 두는 편이 낫다.

