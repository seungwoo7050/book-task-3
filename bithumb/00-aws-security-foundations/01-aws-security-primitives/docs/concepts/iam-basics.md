# IAM 평가 기초

- `explicit deny > allow > implicit deny` 순서를 이해하면 이후 분석 프로젝트도 자연스럽게 이어집니다.
- `Action`과 `Resource`가 모두 맞아야 statement가 적용된다는 점을 테스트로 체감하는 것이 중요합니다.
- wildcard는 편리하지만, 이후 least privilege 관점에서는 broad permission finding의 출발점이 됩니다.
