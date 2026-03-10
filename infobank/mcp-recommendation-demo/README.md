# MCP 추천 데모

`mcp-recommendation-demo/`는 인포뱅크 1번 과제를 학습용으로 풀어낸 트랙이다. 목표는 MCP 추천 문제를 작은 기준선 데모에서 시작해, 비교 실험과 release gate, 운영 콘솔까지 확장하는 흐름을 분명하게 보여 주는 것이다.

## 이 트랙에서 배우는 것

- 추천 품질 기준과 오프라인 평가 계약을 세우는 방법
- MCP catalog와 manifest schema를 운영 가능한 계약으로 고정하는 방법
- 한국어 추천 근거와 차별화 문구를 설계하는 방법
- 사용 로그, feedback, compare, release gate를 통해 개선을 증명하는 방법

## 현재 구조를 읽는 법

- `00~07`: capstone 핵심 설계를 stage별로 나눠 학습할 수 있도록 정리한 pack이다.
- `08/v0`: registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval이 연결된 최초 runnable 데모다.
- `08/v1`: reranker, usage logs, feedback loop, baseline/candidate compare, catalog/experiment CRUD가 추가된 확장 버전이다.
- `08/v2`: compatibility gate, release gate, submission artifact export까지 갖춘 제출 마감 버전이다.
- `08/v3`: self-hosted 운영을 위한 auth, background jobs, audit log, Compose packaging을 더한 OSS hardening 버전이다.

## 처음 읽는 사람에게 권하는 순서

1. `00-source-brief`
2. `02-registry-catalog-and-manifest-schema`
3. `04-selector-baseline-and-reranking`
4. `06-release-compatibility-and-quality-gates`
5. `08-capstone-submission`

바로 결과물을 보고 싶다면 `08-capstone-submission/README.md`와 `08-capstone-submission/v3-oss-hardening/README.md`부터 읽어도 된다.

## 학생용 첫 읽기 경로

- 빠르게 전체 구조를 파악하려면 `08-capstone-submission/README.md`와 상위 `notion/05-development-timeline.md`를 먼저 읽는다.
- 추천 시스템 설계 근육을 따라가려면 `02-registry-catalog-and-manifest-schema`, `04-selector-baseline-and-reranking`, `06-release-compatibility-and-quality-gates` 순서로 내려간다.
- 내 포트폴리오 레포에 옮길 때는 `schema 계약`, `한국어 추천 설명`, `compare`, `release gate` 네 축이 모두 보이도록 정리한다.

## 이 트랙에서 포트폴리오로 가져갈 수 있는 것

- schema-first로 추천 시스템을 설명하는 문서 구조
- 한국어 추천 설명과 운영 콘솔을 함께 다루는 방식
- compare, quality gate, artifact export를 proof artifact로 남기는 법
- self-hosted 확장 버전을 별도 스냅샷으로 유지하는 버전 전략

## notion 문서 정책

- 각 단계의 `notion/`도 레포에 포함한다.
- README, `problem/`, `docs/`는 현재 구조와 검증 경로를 빠르게 안내한다.
- `notion/`은 접근 로그, 시행착오, 회고, 지식 정리를 보관하는 공개 백업 문서다.
- `05-development-timeline.md`는 학생이 제출 버전과 확장 버전을 같은 순서로 다시 재현할 때 기준이 되는 핵심 문서다.
- 새로 다시 쓰고 싶다면 기존 `notion/`을 삭제하지 말고 `notion-archive/`로 옮긴 뒤 새 `notion/`을 만든다.
