# Debug Log

## "인증 로직을 보기도 전에 막혔다"

이 랩에서 만난 가장 답답한 문제는 인증 로직 자체의 버그가 아니었다. **앱을 띄우자마자 테이블이 없어서 아무것도 안 되는 상황**이 반복된 것이다.

처음에는 이렇게 생각했다: "학습 저장소니까 독자가 알아서 `alembic upgrade head`를 먼저 돌려주겠지." 하지만 실제로 해보면, README에 적힌 `make run`을 치자마자 "table users does not exist" 에러가 뜨고 그다음부터 혼란이 시작된다. auth 흐름을 확인하겠다고 프로젝트를 열었는데, 첫 경험이 DB 초기화 트러블슈팅이면 동기 부여가 무너진다.

## 원인을 찾기까지

문제의 핵심은 간단했다. 학습 저장소에서는 **"문서에 적힌 명령이 바로 재현된다"는 것 자체가 요구사항**이라는 점을 놓치고 있었다. 수동 schema 준비 단계를 남겨두면 인증 흐름보다 환경 조립이 먼저 문제가 된다.

## 어떻게 해결했는가

`app/bootstrap.py`에 `initialize_schema()` 함수를 만들어서, 앱이 시작될 때 lifespan hook으로 `Base.metadata.create_all()`을 자동 호출하도록 했다. `app/main.py`의 `lifespan` async context manager에서 이 함수를 부르면, 로컬 개발 환경에서는 별도의 migration 명령 없이도 테이블이 준비된다.

테스트 환경에서도 `conftest.py`에서 `Base.metadata.create_all()`을 직접 호출해서, 각 테스트마다 깨끗한 스키마에서 시작하게 만들었다.

이 변경 이후 `make smoke`와 `docker compose up --build` 모두 추가 수동 단계 없이 바로 동작했다.

## 아직 남아 있는 것

SQLite와 PostgreSQL 사이의 미묘한 차이는 여전히 존재한다. 예를 들어 SQLite에서는 `DateTime(timezone=True)`의 동작이 PostgreSQL과 완전히 같지 않다. 현재는 `now_utc()` 헬퍼에서 명시적으로 UTC `datetime`을 만들어 쓰는 방식으로 우회하고 있지만, PostgreSQL 기반 integration 테스트를 더 늘리면 이 갭을 줄일 수 있다.
