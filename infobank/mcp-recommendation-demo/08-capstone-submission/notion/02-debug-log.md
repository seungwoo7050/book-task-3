# capstone 제출 정리 디버그 기록

## 먼저 확인할 경로

- `README.md`
- `v2-submission-polish/README.md`
- `v2-submission-polish/docs/README.md`
- `v3-oss-hardening/README.md`

## 다시 막히기 쉬운 지점

- `v2`와 `v3`의 역할을 섞어 읽으면 최종 제출 버전이 흐려질 수 있다.
- 버전별 실행 명령을 섞어 쓰면 proof 재현 경로가 꼬일 수 있다.
- 상위 capstone README와 각 버전 README의 설명이 다르면 먼저 상위 문서 기준으로 정렬해야 한다.

## 실제로 다시 확인할 failure pattern

- `v2` 제출 증빙을 만들면서 `v3`의 self-hosted 문서를 먼저 열면, release gate나 artifact export가 필수 범위인지 선택 범위인지 헷갈리기 쉽다.
- `compare`, `compatibility`, `release gate` proof 문서를 따로 읽으면 각 명령이 같은 release candidate를 기준으로 실행돼야 한다는 점을 놓치기 쉽다.
- `05-development-timeline.md`를 건너뛰고 버전 README만 훑으면, 왜 `v0 -> v1 -> v2` 순서로 범위를 넓혔는지 재현 이유가 약해진다.

## 이번에 적용한 정렬 기준

- 상위 capstone README에서 `v2`를 제출 기준선, `v3`를 확장/OSS 분기로 먼저 못 박는다.
- 각 proof 문서에는 어떤 명령으로 검증하는지 직접 적어 두어 문서 간 왕복 비용을 줄인다.
- notion의 timeline과 tracked docs의 stable index 역할을 분리해, "설명"과 "재현"이 서로 충돌하지 않게 한다.
