# Repository Improvement Roadmap

2026-03-08 기준으로 초기 개선 로드맵은 완료됐다.
이 문서는 더 이상 부족한 슬롯을 채우는 계획이 아니라, 현재 검증된 학습 경로의 유지 기준을 적는다.

## Guiding Rule

- 새 프로젝트를 추가하기 전에 기존 경로의 학습 이유가 충분히 분리되어 있는지 먼저 확인한다.
- 각 프로젝트는 `문제`, `구현`, `검증`, `문서`, `notion/`이 함께 유지돼야 한다.
- 루트 상태 문서와 검증 스크립트가 실제 구현 상태와 어긋나면 즉시 수정한다.

## Completed Spine

현재 검증된 학습 경로는 다음과 같다.

- Foundations: `navigation`, `virtualized-list`, `gestures`
- Architecture: `bridge-vs-jsi`, `native-modules`
- Product Systems: `offline-sync-foundations`, `realtime-chat`, `app-distribution`
- Capstone: `incident-ops-mobile`, `incident-ops-mobile-client`

## Maintenance Priorities

### 1. Keep Verification Alive

대상:

- 모든 `problem/Makefile`
- 루트 검증 스크립트
- 프로젝트별 README 명령 집합

Definition of Done:

- `bash scripts/report_study_status.sh` 결과가 모든 프로젝트를 `verified`로 보여 준다.
- `bash scripts/verify_study_structure.sh`와 `bash scripts/check_study_docs.sh`가 계속 통과한다.
- 새 변경이 들어와도 `problem/Makefile`의 canonical command가 깨지지 않는다.

### 2. Refresh Demo Artifacts

대상:

- `virtualized-list` benchmark summary
- `app-distribution` release rehearsal summary
- `incident-ops-mobile` demo artifacts
- `incident-ops-mobile-client` portfolio captures

Definition of Done:

- 산출물이 프로젝트 로컬 경로에 기록된다.
- README와 docs가 산출물 경로를 정확히 가리킨다.
- 오래된 캡처나 summary가 현재 코드와 어긋나지 않는다.

### 3. Only Add New Projects For Real Gaps

대상:

- 미래에 추가될 새 학습 프로젝트

Definition of Done:

- 새 프로젝트가 기존 프로젝트를 대체하지 않고, 명확한 pedagogical gap을 메운다.
- 추가 이유가 `docs/curriculum-map.md`와 루트 문서에 설명된다.
- 공개 코드, 검증 명령, docs, notion 구조를 갖추지 못하면 새 슬롯을 만들지 않는다.

## Stop Doing

- 상태 문서가 실제 구현보다 뒤처진 채 남는 일
- demo/release artifact를 프로젝트 밖 임의 경로에 흩뿌리는 일
- 문서만 있고 실행 증거가 없는 프로젝트를 새로 늘리는 일
