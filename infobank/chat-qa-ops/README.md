# Chat QA Ops 트랙

`chat-qa-ops/`는 인포뱅크 2번 과제를 학습용으로 풀어낸 트랙이다. 목표는 상담 챗봇 자체를 만드는 것이 아니라, 답변 품질을 정의하고 자동으로 평가하고 모니터링하는 QA Ops 계층을 단계적으로 익히는 데 있다.

## 이 트랙에서 배우는 것

- 상담 품질을 rubric과 score contract로 정의하는 방법
- 규칙 기반 guardrail과 근거 검증을 함께 쓰는 방법
- golden set과 compare artifact로 개선을 증명하는 방법
- 운영 대시보드와 self-hosted 데모까지 연결하는 방법

## 현재 구조를 읽는 법

- `00~07`: 개념을 잘게 나눈 학습용 stage pack이다.
- `08/v0`: 가장 빠르게 재현 가능한 baseline 데모다.
- `08/v1`: provider chain, lineage/trace, PostgreSQL smoke path를 더한 안정화 버전이다.
- `08/v2`: 개선 실험과 compare artifact를 갖춘 제출 마감 버전이다.
- `08/v3`: 로그인, 업로드, 비동기 job, Docker Compose quickstart까지 포함한 self-hosted OSS snapshot이다.

## 처음 읽는 사람에게 권하는 순서

1. `00-source-brief`
2. `03-rule-and-guardrail-engine`
3. `06-golden-set-and-regression`
4. `08-capstone-submission`
5. `08-capstone-submission/v3-self-hosted-oss`

바로 실행 가능한 결과물을 먼저 보고 싶다면 `08-capstone-submission/v3-self-hosted-oss`부터 시작해도 된다.

## 학생용 첫 읽기 경로

- 빠르게 감을 잡고 싶다면 `08-capstone-submission/README.md`와 상위 `notion/05-development-timeline.md`를 먼저 읽는다.
- 왜 이런 구조가 됐는지 알고 싶다면 `00-source-brief`, `03-rule-and-guardrail-engine`, `06-golden-set-and-regression` 순서로 되돌아간다.
- 내 포트폴리오 레포에 옮길 때는 `score contract`, `failure taxonomy`, `proof artifact`, `운영 대시보드` 네 축이 모두 남는지 확인한다.

## 이 트랙에서 포트폴리오로 가져갈 수 있는 것

- 품질 기준표와 score contract를 어떻게 공개 문서로 쓰는지
- failure taxonomy와 evidence trace를 어떻게 proof artifact로 연결하는지
- stage pack에서 capstone 버전 스냅샷으로 넘어가는 정리 방식
- self-hosted 데모까지 포함할 때 README가 어디까지 안내해야 하는지

## notion 문서 정책

- 각 단계의 `notion/`도 레포에 포함한다.
- `README.md`, `problem/`, `docs/`는 빠른 길찾기와 현재 상태 설명을 맡는다.
- `notion/`은 판단 과정, 실패 기록, 회고, 지식 인덱스를 담는 공개 백업 문서다.
- `05-development-timeline.md`는 학생이 같은 검증 흐름을 다시 따라가거나 자기 레포에 재구성할 때 가장 먼저 보는 문서다.
- 새로 다시 쓰고 싶다면 기존 `notion/`을 지우지 말고 `notion-archive/`로 옮긴 뒤 새 `notion/`을 만든다.

## 더 읽을 문서

- [`release-readiness.md`](./release-readiness.md)
- [`08-capstone-submission/README.md`](./08-capstone-submission/README.md)
