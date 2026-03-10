# 회고

## v2에서 얻은 것

- “왜 이 서비스를 분리했는가”를 코드와 문서로 같이 설명할 수 있게 됐다.
- v1에서는 내부 모듈 경계였던 것이, v2에서는 gateway, identity, workspace, notification의 별도 실행 단위로 드러난다.
- comment 저장, 알림 소비, websocket fan-out, edge API 유지가 서로 다른 책임이라는 점이 한 프로젝트 안에서 보인다.

## v2에서 잃은 것

- 로컬 테스트가 무거워졌다.
- 단순한 댓글 알림 하나도 gateway, outbox, stream, consumer, pub/sub를 통과해야 한다.
- 서비스별 health, env, dependency, cleanup까지 따로 챙겨야 하므로 구현보다 운영 문서 비중이 커졌다.

## 이 비용을 어떻게 해석할 것인가

이 비용을 숨기지 않고 적는 편이 오히려 학습 레포답다. v2는 “운영급 MSA 완성본”이 아니라 “왜 이런 구조가 생기는가를 보여 주는 학습판”이어야 한다.

## 다음에 보강할 부분

- contract versioning 규칙
- retry policy와 dead letter 문서
- trace backend와 상호관계 시각화
- 실제 배포 자동화와 문서 수준 target shape의 경계
