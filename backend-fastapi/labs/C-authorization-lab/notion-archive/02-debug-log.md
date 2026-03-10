# Debug Log

## Bootstrap 없이 시작했을 때의 실패

이 랩은 Alembic 마이그레이션이 compose.yaml에 자동으로 포함되어 있지 않다. A-auth-lab처럼 `alembic upgrade head`를 compose 시작 명령에 넣을 수도 있지만, 이 랩에서는 `bootstrap.py`의 `initialize_schema()`가 `Base.metadata.create_all()`로 스키마를 생성한다.

문제는 `main.py`의 startup에서 이 bootstrap이 호출되는지 여부다. 로컬 개발 시 SQLite에서는 파일이 없으면 자동 생성되므로 눈에 띄지 않지만, Docker Compose에서 PostgreSQL을 쓸 때 테이블이 미리 생성되어 있지 않으면 첫 번째 API 호출에서 `ProgrammingError: relation "users" does not exist`가 발생한다.

해결: bootstrap을 startup에서 호출하도록 유지하거나, compose 명령에 마이그레이션을 포함한다. conftest에서는 `Base.metadata.create_all()`로 매 테스트마다 깨끗한 스키마를 보장한다.

## Invite Accept 시 이메일 불일치 에러

초기 테스트에서 invite를 만들 때 email을 "Viewer@example.com"으로, user를 만들 때 email을 "viewer@example.com"으로 설정해서 불일치가 발생했다. 코드에서 `email.lower()`로 정규화하는 위치가 `create_user`와 `create_invite` 두 곳에 있어야 일관성이 유지된다. 테스트를 수정하기보다 서비스 레이어에서 항상 소문자로 저장하도록 보장했다.

## Viewer가 문서를 생성할 수 있는 버그

최초 구현에서 `create_document`의 `_require_role`에 `minimum="viewer"`로 잘못 설정한 적이 있었다. viewer도 문서를 생성할 수 있게 된 것이다. 테스트에서 `forbidden.status_code == 403`이 깨져서 발견했다. `minimum="member"`로 수정하여 viewer는 읽기만, member 이상은 쓰기 가능이라는 경계를 복구했다.

이 경험에서 배운 것: **forbidden-path 테스트가 없으면 권한 규칙의 하한선이 보이지 않는다.** 정상 경로만 테스트하면 "허용되어야 할 것이 허용됨"만 확인하고, "차단되어야 할 것이 차단됨"은 놓친다.
