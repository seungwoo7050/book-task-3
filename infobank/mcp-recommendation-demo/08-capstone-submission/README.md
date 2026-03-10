# 08 capstone 제출 정리

이 트랙은 `MCP 추천 최적화`를 운영형 시스템으로 완성하는 capstone archive다. `v0 -> v2`는 제출용 capstone 본선이고, `v3`는 `v2`를 self-hosted OSS 후보로 확장한 제품화 버전이다.

## 버전을 왜 나눴는가

- `v0-initial-demo`: registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable 데모
- `v1-ranking-hardening`: reranker, usage logs, feedback loop, baseline/candidate compare, catalog/experiment CRUD를 추가한 운영형 추천 버전
- `v2-submission-polish`: compatibility gate, release gate, submission artifact export를 갖춘 최종 capstone 데모
- `v3-oss-hardening`: auth, background jobs, audit log, Compose deployment를 더한 OSS hardening 버전

모든 버전은 폴더 단위 스냅샷이며, 이전 버전을 덮어쓰지 않는다.

## 먼저 읽을 순서

1. [`docs/README.md`](./docs/README.md)
2. [`v2-submission-polish/README.md`](./v2-submission-polish/README.md)
3. [`v3-oss-hardening/README.md`](./v3-oss-hardening/README.md)
4. 필요하면 `v0`, `v1`로 내려가 baseline과 hardening 과정을 본다

그다음에는 상위 [`notion/05-development-timeline.md`](./notion/05-development-timeline.md)를 읽어 어떤 순서로 증빙을 재현하고 비교해야 하는지 맞춘다.

## 이 capstone에서 포트폴리오로 가져갈 것

- schema, 추천 로직, feedback loop, release gate를 하나의 추천 시스템 설명으로 묶는 방식
- compare와 artifact export를 개선 증빙으로 제시하는 방식
- 최종 제출 버전과 self-hosted 확장 버전을 분리하는 버전 전략
- 운영 콘솔과 배포 문서를 함께 갖춘 README 구성

## 발표 자료와 노트

- `v0`, `v1`, `v2`, `v3`는 각각 발표 문서와 시연 자료를 가진다.
- 발표에서는 `v2`를 최종 capstone으로 먼저 설명하고, `v3`는 "실제로 설치해서 쓰려면 무엇이 더 필요한가"를 답하는 확장 버전으로 다룬다.
- `notion/`은 이 capstone의 공개 백업 노트이며, `05-development-timeline.md`가 제출 재현의 기준 문서다.
- 다시 쓸 때는 기존 폴더를 `notion-archive/`로 보존한다.
