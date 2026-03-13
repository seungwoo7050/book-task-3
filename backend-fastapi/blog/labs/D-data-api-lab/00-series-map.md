# D-data-api-lab

이 글은 프로젝트, 태스크, 댓글 API를 만들 때 단순 CRUD보다 어떤 데이터 일관성 규칙을 먼저 드러내야 하는가를 묻는다. D 랩은 기능 수를 늘리기보다 목록 semantics, 소프트 삭제, 동시 수정 충돌 같은 현실적인 데이터 문제를 먼저 표면으로 올린다.

## 이 글이 붙잡는 질문
데이터 중심 API에서 생성과 조회만 잘 되는 것으로 충분하지 않다면, 필터링과 정렬, 삭제 정책, optimistic locking 가운데 무엇을 먼저 API surface로 설명해야 하는가가 이 글의 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 problem 문서가 데이터 API의 성공 기준을 명시하고, 통합 테스트는 목록 조건과 버전 충돌, 하위 리소스 생성을 한 흐름으로 묶는다. 덕분에 이 프로젝트는 단순 예제가 아니라 데이터 일관성을 읽는 독립 단위가 된다.

## 이번 글에서 따라갈 흐름
1. 데이터 API를 CRUD보다 넓은 문제로 다시 정의한다.
2. 목록 조건과 버전 필드를 route surface로 끌어올린다.
3. 충돌과 소프트 삭제를 테스트로 문서화한다.
4. 재검증 기록으로 compose와 health surface까지 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py::update_project`
- 테스트/런타임: `labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py::test_optimistic_locking_and_task_comment_creation`
- CLI: `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/D-data-api-lab/fastapi 8002`

## 이 글을 다 읽고 나면
- 필터링, 정렬, 페이지네이션이 도메인 해석에 어떤 영향을 주는지 감이 잡힌다.
- 소프트 삭제와 optimistic locking이 왜 함께 자주 등장하는지 이해하게 된다.
- 버전 필드 하나가 API 계약을 어떻게 바꾸는지 볼 수 있다.
- 검증 기록: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다.
- 다음으로 이어 볼 대상: E-async-jobs-lab
