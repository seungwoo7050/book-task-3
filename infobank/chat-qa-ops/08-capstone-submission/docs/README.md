# 08 capstone 문서 안내

이 디렉터리는 capstone 버전 공통 문서와 시연 자료를 보관하는 stable index다.

## 버전별 역할

- `v0-*`: runnable baseline과 local heuristic path 정리
- `v1-*`: provider fallback, lineage/trace, PostgreSQL smoke, version compare hardening
- `v2-*`: retrieval improvement proof와 제출용 artifact 마감
- `v3-*`: self-hosted OSS 후보로 확장한 운영/배포 경로 정리

## 이 디렉터리에서 오래 남길 개념

- immutable version snapshots
- provider fallback chain
- trace-rich evaluation pipeline
- run-level version compare
- RAG improvement proof

## 검증 메모

- `v0`, `v1`, `v2` 모두 `UV_PYTHON=python3.12 make gate-all`을 통과시켰다.
- `v1`, `v2`에서 `make smoke-postgres`를 통과시켰다.
- baseline/candidate compare 결과는 `avg_score 84.06 -> 87.76`, `critical 2 -> 0`, `pass 16 -> 19`, `fail 14 -> 11`이다.

## 먼저 읽을 순서

- `README.md`
- `docs/release-readiness.md`
- `v0-initial-demo/README.md`, `v1-regression-hardening/README.md`, `v2-submission-polish/README.md`
- `v2-submission-polish/docs/demo/proof-artifacts/`
- 필요하면 `v3-self-hosted-oss/README.md`로 확장 방향을 본다.

## 노트 운영 원칙

- live Upstage/OpenAI/Langfuse credential path는 기본 검증에 포함되지 않았다.
- tracked 문서는 stable index 역할을 하고, `notion/`은 판단 과정과 회고를 담는 공개 백업 문서다.
- capstone 노트를 다시 정리할 때는 기존 `notion/`을 `notion-archive/`로 옮겨 보존한다.

## 학생이 이 문서 묶음에서 바로 가져갈 것

- `README.md`, `problem/README.md`, `docs/README.md`, `notion/05-development-timeline.md`를 서로 다른 공개 역할로 나누는 방식
- 현재 단계의 검증 명령과 acceptance 기준을 짧은 공개 문서로 남기는 방식
- 장문 시행착오는 `notion/`으로 보내고, 오래 남길 개념과 증빙만 tracked docs에 남기는 방식

## notion과 05 타임라인을 읽는 법

- 빠른 현재 상태는 tracked docs에서 먼저 확인한다.
- 같은 결과를 다시 재현하려면 `../notion/05-development-timeline.md`를 따라 읽고 실행한다.
- 새 기준으로 다시 쓰고 싶다면 기존 `notion/`을 `../notion-archive/`로 옮긴 뒤 새 `notion/`을 만든다.
