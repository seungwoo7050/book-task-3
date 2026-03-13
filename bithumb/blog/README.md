# bithumb blog

이 디렉터리는 `bithumb/`의 10개 독립 프로젝트를 `blog-writing-guide.md` 기준으로 다시 쓴 source-first 블로그 시리즈입니다.

## 이 블로그 계층의 기준

- `notion/`과 `notion-archive/`는 읽지 않습니다.
- `README.md`, `problem/README.md`, `python/README.md`, `docs/`, `python/src/`, `python/tests/`, `Makefile`, `pyproject.toml`, `docker-compose.yml`, `git log/show`, 실제 재검증 명령만 근거로 사용합니다.
- 정확한 과거 작업 시각이 부족한 구간은 `Day / Session` 형식으로 적고, commit 날짜는 `Git Anchor`로만 제한해 둡니다.
- 코드는 판단이 갈린 짧은 핵심 조각만 남기고, CLI는 현재 레포에서 다시 실행 가능한 경로를 chronology 순서대로 정리합니다.

## 현재 범위

- [00 AWS Security Foundations](00-aws-security-foundations/README.md): IAM 판단 규칙, Terraform plan, CloudTrail 정규화처럼 후속 분석이 기대하는 입력을 고정하는 트랙입니다.
- [01 Cloud Security Core](01-cloud-security-core/README.md): finding, remediation, detection, governance를 작은 도구 단위로 쌓는 트랙입니다.
- [02 Capstone](02-capstone/README.md): 앞선 프로젝트를 API, worker, DB, report 흐름으로 다시 묶는 최종 통합 트랙입니다.

## 검증 스냅샷

- `2026-03-13 make test-unit`: 8개 단위 프로젝트 테스트가 모두 통과했습니다. 총 18개 테스트가 `01 3`, `03 1`, `04 3`, `05 3`, `06 2`, `07 2`, `08 2`, `09 2`로 나뉘어 확인됐습니다.
- `2026-03-13 make test-integration`: Terraform 기반 02번 프로젝트 테스트 3개가 통과했습니다.
- `2026-03-13 make test-capstone`: capstone end-to-end 테스트 1개가 통과했습니다.
- `2026-03-13 make demo-capstone`: `02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo`에 demo 산출물이 생성됐습니다.

## 읽는 순서

1. 루트 [README.md](../README.md)에서 전체 트랙 순서와 검증 표면을 먼저 확인합니다.
2. 원하는 트랙의 blog index로 내려가 각 프로젝트 `00-series-map.md`를 먼저 읽습니다.
3. 그다음 chronology 문서에서 실제 소스와 테스트가 어떤 순서로 읽히는지 따라갑니다.
4. 원래 프로젝트 문서가 필요하면 series map의 근거 파일 링크로 바로 이동합니다.
