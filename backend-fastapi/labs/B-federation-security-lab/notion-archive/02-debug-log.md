# Debug Log

## DB 이름 불일치: 인프라 설정에서 시작된 실패

federation 랩의 첫 번째 문제는 코드가 아니라 인프라 설정이었다. `compose.yaml`에서 PostgreSQL 컨테이너의 `POSTGRES_DB`가 `b_federation_security_lab`으로 되어 있는데, 애플리케이션의 `.env`나 `Settings`에 기록된 `DATABASE_URL`이 이 이름과 정확히 일치하지 않으면 연결이 실패한다.

문제의 은밀한 점은, SQLite 모드로 로컬 개발을 하다가 Docker Compose로 전환할 때 드러난다는 것이다. 로컬에서 `sqlite+pysqlite:///./b_federation_security_lab.db` 기본값으로 잘 돌아가던 것이 Compose 환경에서 PostgreSQL URL로 바뀌면 DB 이름이 정확히 맞아야 한다. 이름이 한 글자만 달라도 `psycopg` 연결이 "database does not exist"로 실패한다.

수정은 단순했다—Compose의 `POSTGRES_DB`와 앱 설정의 `DATABASE_URL` 경로를 동일하게 맞추는 것. 하지만 이 경험에서 얻은 교훈은 명확하다: **외부 개념(federation, OIDC, 2FA)이 많은 프로젝트일수록, 기본적인 인프라 정합성 확인을 먼저 해야 한다.** OIDC 로직을 디버깅하기 전에 DB 연결이 되는지부터 확인하라.

## OAuth State Cookie 누락 문제

테스트 초기에 callback 엔드포인트가 "OAuth state cookie is missing" 에러를 반환하는 경우가 있었다. 원인은 `TestClient`의 쿠키 처리 방식이었다. `GET /google/login`이 `oauth_state` 쿠키를 설정하는데, `TestClient`가 이 쿠키를 후속 요청에 자동으로 포함하지 않는 경우가 발생할 수 있다.

해결 방법은 `TestClient`를 context manager로 사용하고(`with TestClient(app) as client`), 같은 client 인스턴스로 login과 callback을 순차적으로 호출하는 것이다. conftest의 `client` fixture가 정확히 이 패턴을 따른다.

## pending_auth_token과 access_token의 혼동

2FA 활성 사용자의 callback 응답에서 `clear_auth_cookies`를 먼저 호출하고 `set_pending_auth_cookie`를 설정하는 순서가 중요했다. 초기에는 이전 세션의 access_token 쿠키가 남아 있어서, 2FA 챌린지 중인데도 `GET /me`가 200을 반환하는 문제가 있었다. callback에서 모든 인증 쿠키를 먼저 지우고, 상태에 따라 pending_auth 또는 access/refresh를 새로 설정하는 순서로 해결했다.

## Rate Limiter 메모리 누수 가능성

테스트에서 `RateLimiter._memory_store`가 class-level dict이기 때문에, 테스트 간에 상태가 공유되는 문제가 있었다. conftest에서 `RateLimiter._memory_store.clear()`를 fixture 시작 시 호출하여 해결했다. 이것은 in-memory fallback 모드에서만 발생하는 문제이고, Redis 사용 시에는 키 만료로 자연 해소된다.
