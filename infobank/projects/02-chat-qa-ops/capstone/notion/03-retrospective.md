# capstone 회고

## 이번 stage로 강화된 점

- 구현, 테스트, proof artifact, public docs가 서로 연결되어 있다.
- 버전별 학습 목적과 변경 범위가 명확하다.

## 아직 약한 부분

- external provider와 observability stack은 mock/no-op 검증이 주 경로다.
- notion 문서는 공개 백업 문서이지만, 빠른 현재 상태 확인은 tracked docs를 먼저 읽는 편이 낫다.

## 학생이 여기서 바로 가져갈 것

- stage 학습 결과를 `v0 -> v3` 스냅샷으로 묶어 공개 저장소에서 설명하는 방식
- proof artifact, release readiness, self-hosted 확장을 같은 레포 안에서 역할별 문서로 나누는 방식

## 다음 stage로 넘기는 자산

- immutable version snapshots
- provider fallback chain
- trace-rich evaluation pipeline
- run-level version compare
- RAG improvement proof

## 05-development-timeline.md와 같이 읽을 포인트

- 먼저 `v2`를 제출 기준선으로 재현하고, 그 뒤에 `v0`, `v1`, `v3`를 비교하는 순서를 유지한다.
- 자기 포트폴리오 레포로 옮길 때도 이 버전 분리 전략을 그대로 가져가면 설명력이 높아진다.

## 나중에 다시 볼 것

- 실제 Upstage/OpenAI/Langfuse 자격증명이 준비되면 live smoke run 문서를 별도 부록으로 추가할 수 있다.
- dashboard screenshots를 자동 재생성하는 스크립트를 붙이면 proof artifact 갱신이 더 쉬워진다.
