# Problem Framing

## ORM은 마법이 아니라 계약이다

앞선 세 랩은 "이 사람이 누구인가"와 "이 사람이 무엇을 할 수 있는가"를 다뤘다. 이 랩은 그 다음 질문으로 넘어간다—**데이터를 어떻게 읽고, 쓰고, 바꾸고, 지울 것인가.** CRUD라고 부르는 이 네 동작은 단순해 보이지만, 실무에서는 항상 조건이 붙는다. 목록을 보여줄 때 필터링과 정렬이 필요하고, 한 페이지에 모든 데이터를 내려줄 수 없으니 페이지네이션이 필요하고, 두 사람이 동시에 같은 레코드를 수정하면 누구의 변경이 살아남을지 결정해야 한다.

이 랩의 목표는 프로젝트(Project) → 태스크(Task) → 코멘트(Comment)라는 세 모델 위에서 이 문제들을 하나씩 드러내는 것이다. SQLAlchemy ORM을 사용하되, ORM이 자동으로 해주는 것과 명시적으로 코드에서 관리해야 하는 것의 경계를 분명히 한다.

## 핵심 주제

다섯 가지 데이터 관심사가 이 랩의 중심이다:

1. **CRUD**: Project, Task, Comment의 생성/조회/수정/삭제
2. **Filtering**: status 필드로 active/archived 필터링
3. **Sorting**: title 기준 오름차순/내림차순 (sort=title, sort=-title)
4. **Page-based Pagination**: page + page_size 쿼리 파라미터, total count 반환
5. **Optimistic Locking**: version 필드로 stale update 감지 → 409 Conflict
6. **Soft Delete**: deleted_at 타임스탬프로 논리 삭제, include_deleted 옵션으로 복구 가능성 유지

## 제약 조건

- 인증과 권한이 없다. 누구든 API를 호출할 수 있다.
- Cursor-based pagination은 다루지 않는다. Page-based의 한계를 인지하되, 먼저 개념을 명확히 한다.
- 검색(full-text search)은 범위 밖이다.
- 프레임워크: FastAPI + SQLAlchemy 2.0, PostgreSQL 16
- 포트: API 8002, PostgreSQL 5434

## 성공 기준

- `GET /projects?status=active&sort=title&page=1&page_size=1` → 필터+정렬+페이징이 동시 작동
- `PATCH /projects/{id}` + 올바른 version → 200, 틀린 version → 409
- `DELETE /projects/{id}` → soft delete (deleted_at 설정, version 증가)
- soft delete된 프로젝트가 기본 목록에서 제외, `include_deleted=true` 시 포함
- `POST /projects/{id}/tasks` → 삭제된 프로젝트에는 task 생성 불가
- `make lint`, `make test`, `make smoke`, Compose probe 통과
