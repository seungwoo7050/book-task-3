# Chat QA Ops 최종 제출 정리

이 capstone은 상담 품질 평가 파이프라인과 운영 대시보드를 묶어 제출 가능한 데모로 마감하는 프로젝트다. stage별로 분리해 익힌 계약, 규칙, trace, regression, dashboard를 실제 버전 스냅샷으로 다시 묶어 보여 준다.

## 버전을 왜 나눴는가

1. `v0-initial-demo`: 최초 제출 가능한 QA Ops baseline 데모
2. `v1-regression-hardening`: `v0`를 안정화하고 lineage, compare, PostgreSQL 검증 경로를 더한 버전
3. `v2-submission-polish`: 개선 실험 증빙과 제출 시연 자료를 정리한 마감 버전
4. `v3-self-hosted-oss`: `v2`를 single-team self-hosted OSS snapshot으로 확장한 버전

모든 버전은 폴더 단위 스냅샷이다. 이전 버전을 덮어쓰지 않고, 다음 버전 폴더를 복제해 역할을 분리한다.

## 먼저 읽을 순서

1. [`docs/release-readiness.md`](./docs/release-readiness.md)
2. [`docs/README.md`](./docs/README.md)
3. [`v2-submission-polish/README.md`](./v2-submission-polish/README.md)
4. [`v3-self-hosted-oss/README.md`](./v3-self-hosted-oss/README.md)

발표 자료나 시연 흐름이 필요하면 [`docs/presentations/README.md`](./docs/presentations/README.md)로 이어서 읽는다.

그다음에는 상위 [`notion/05-development-timeline.md`](./notion/05-development-timeline.md)를 읽어 어떤 순서로 버전을 재현해야 하는지 맞춘다.

## 이 capstone에서 포트폴리오로 가져갈 것

- 버전 스냅샷으로 개선 과정을 보존하는 방법
- 공개 저장소 기준 검증 명령과 proof artifact를 함께 적는 방식
- "학습용 stage pack"과 "보여 줄 수 있는 제출물"을 하나의 레포 안에서 연결하는 방식
- self-hosted 확장을 별도 버전으로 떼어 제품화 방향을 설명하는 방식

## notion 정책

- `notion/`은 이 capstone의 공개 백업 노트다.
- `05-development-timeline.md`는 제출 재현과 자기 포트폴리오 재구성을 동시에 돕는 기준 문서다.
- 새 기준으로 다시 쓸 때는 기존 `notion/`을 `notion-archive/`로 옮겨 두고 새 `notion/`을 만든다.
- 빠른 현재 상태 확인은 먼저 README와 `docs/`를 보고, 더 자세한 판단 과정은 `notion/`에서 본다.
