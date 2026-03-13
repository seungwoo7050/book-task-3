# D-data-api-lab Structure Plan

## 한 줄 약속
- CRUD를 만들되, 목록 조건과 충돌 제어를 먼저 드러내기

## 독자 질문
- 프로젝트, 태스크, 댓글 API를 만들 때 단순 생성/조회보다 어떤 데이터 일관성 surface를 먼저 드러낼 것인가.
- 엔터티 관계를 어디까지 API에 그대로 드러낼 것인가 소프트 삭제는 목록 조회에서 어떤 의미를 가지는가 optimistic locking은 어떤 충돌을 막아 주는가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 데이터 API를 단순 CRUD보다 넓은 문제로 잡기
2. 목록 조건과 버전 필드를 route surface에 올리기
3. 충돌과 소프트 삭제를 테스트로 굳히기
4. 2026-03-09 재검증으로 Compose surface까지 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py::update_project` — 버전 필드를 통해 optimistic locking이 API surface로 드러나는 지점이다.
- 보조 앵커: `labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py::test_optimistic_locking_and_task_comment_creation` — 버전 충돌과 하위 task/comment 생성이 같은 흐름 안에서 만난다.
- 문서 앵커: `labs/D-data-api-lab/problem/README.md`, `labs/D-data-api-lab/docs/README.md`
- CLI 앵커:
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 글에서 강조할 개념
- service boundary와 repository 역할 page-based pagination의 한계와 장점 충돌 감지와 버전 필드의 의미
- 프로젝트, 태스크, 댓글 API 설계 서비스 계층과 ORM 경계 정리 필터링, 정렬, 페이지 기반 페이지네이션 인증/인가를 붙이지 않고 데이터 경계에 집중합니다. 페이지네이션은 cursor 대신 page-based 모델로 유지합니다.

## 끝맺음
- 제외 범위: 인증과 인가 전문 검색이나 대규모 인덱싱 복잡한 이벤트 소싱이나 CQRS
- 검증 문장: 2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다.
