# capstone 제출 정리 접근 기록

## 선택한 방향

- 최종 capstone을 한 번에 덮어쓰지 않고 버전 스냅샷으로 유지했다.
- `v2`를 최종 제출 버전으로, `v3`를 제품화 확장 버전으로 분리했다.
- 추천 기준, 데이터 계약, compare proof, release gate, self-hosted 확장을 한 줄기로 설명하도록 구성했다.

## 버전별 역할

- - `v0-initial-demo`: registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable 데모다.
- - `v1-ranking-hardening`: v0를 바탕으로 reranker, usage logs, feedback loop, baseline/candidate compare를 더한 운영형 추천 버전이다.
- - `v2-submission-polish`: v1를 바탕으로 compatibility gate, release gate, artifact export, 제출용 proof 문서를 더해 최종 capstone으로 마감한 버전이다.
- - `v3-oss-hardening`: self-hosted OSS 후보로 확장한 productization 버전

## 이번에 버린 선택

- 하나의 폴더에서 모든 변화를 덮어쓰는 방식
- self-hosted 확장과 제출용 마감을 같은 버전에서 동시에 설명하는 방식
- 발표 자료와 실행 경로를 따로 놀게 두는 방식
