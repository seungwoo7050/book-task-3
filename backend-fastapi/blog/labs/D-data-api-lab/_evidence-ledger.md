# D-data-api-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README와 problem 문서가 필터링, 정렬, 페이지네이션, 소프트 삭제, optimistic locking을 명시하고, `tests/integration/test_data_api.py`가 그 네 축을 한 번에 검증한다.
- 프로젝트 질문: 프로젝트, 태스크, 댓글 API를 만들 때 단순 생성/조회보다 어떤 데이터 일관성 surface를 먼저 드러낼 것인가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/D-data-api-lab/README.md`
- `labs/D-data-api-lab/problem/README.md`
- `labs/D-data-api-lab/docs/README.md`
- `labs/D-data-api-lab/fastapi/README.md`
- `labs/D-data-api-lab/fastapi/Makefile`
- `labs/D-data-api-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py`
- `backend-fastapi/labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py`
- `git log -- backend-fastapi/labs/D-data-api-lab`

## 프로젝트 표면 요약
- 문제 요약: 프로젝트, 태스크, 댓글을 다루는 데이터 중심 API를 만든다고 가정합니다. 단순 CRUD를 넘어서, 목록 조회 조건, 삭제 정책, 동시 수정 충돌 같은 현실적인 데이터 API 문제를 같이 다뤄야 합니다. 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다. 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다. 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다. 소프트 삭제가 목록 조회에 반영되어야 합니다. 낙관적 락으로 충돌을 감지하는 경로가 있어야 합니다.
- 설계 질문: 엔터티 관계를 어디까지 API에 그대로 드러낼 것인가 소프트 삭제는 목록 조회에서 어떤 의미를 가지는가 optimistic locking은 어떤 충돌을 막아 주는가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | 프로젝트/태스크/댓글 API의 최소 제품 표면 정의 | README.md, problem/README.md, docs/README.md | CRUD만 돌아가면 데이터 API 랩으로 충분할 것 | 필터링, 정렬, 페이지네이션, 소프트 삭제, optimistic locking을 성공 기준에 포함 | README의 `make run`, `docker compose up --build` | 문제 정의가 단순 CRUD보다 조회 조건과 충돌 감지를 먼저 적음 | problem/README.md 성공 기준 | 데이터 API의 난점은 생성보다 목록과 충돌에서 더 자주 드러난다 | 버전 필드를 API contract로 올리기 |
| 2 | Phase 2, route/service/repository 의존성으로 복원 | page-based pagination과 optimistic locking을 route contract에 노출 | app/api/v1/routes/data_api.py, app/domain/services/data_api.py, app/repositories/data_repository.py | 충돌 제어는 repository 내부에만 숨겨도 괜찮을 것 | `update_project` payload에 version을 받고, list endpoint에 filter/sort/page 파라미터를 고정 | `make test` | `update_project`가 title/status와 함께 version을 받음 | app/api/v1/routes/data_api.py::update_project | 낙관적 락은 내부 구현이 아니라 API를 쓰는 클라이언트가 알아야 하는 계약이다 | 삭제와 충돌 실패를 테스트로 고정 |
| 3 | Phase 3, 테스트가 목록 의미를 확정 | soft delete, include_deleted, stale version 409를 실제 요청으로 검증 | tests/integration/test_data_api.py | 정상 CRUD 시나리오만 있으면 데이터 경계가 충분히 보일 것 | 활성 목록 필터, 삭제 후 숨김, include_deleted 재노출, stale update 409를 테스트화 | `make test` | active 목록에서 Beta가 사라지고, stale version update는 409를 반환 | tests/integration/test_data_api.py::test_filter_sort_pagination_and_soft_delete | 데이터 API는 저장보다 조회 semantics를 테스트로 고정할 때 설명력이 생긴다 | 실제 실행 surface 점검 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | 문서에 적힌 데이터 API가 실제 재실행된다는 사실 확인 | docs/verification-report.md, .github/workflows/labs-fastapi.yml, tools/compose_probe.sh | 테스트 파일만 있으면 프로젝트 독립성이 충분할 것 | compile, lint, test, smoke, Compose probe와 스키마 자동 초기화 메모를 남김 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/D-data-api-lab/fastapi 8002` | 2026-03-09 기준 재검증 통과, 앱 시작 시 스키마 자동 초기화 기록 | docs/verification-report.md D-data-api-lab 항목 | 데이터 API도 결국 HTTP health surface가 살아 있어야 독립 프로젝트가 된다 | 비동기 작업으로 경계 확장 |
