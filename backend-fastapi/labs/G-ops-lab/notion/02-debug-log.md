# 디버그 기록: 운영 코드에서 만난 문제들

## 문제 1: Compose healthcheck와 의존성 순서

### 증상

`docker compose up --build`로 시작하면 API가 올라오기 전에
healthcheck가 실패해서 `unhealthy` 상태가 나타났다.

### 원인

healthcheck의 `start_period`가 너무 짧았다.
FastAPI 앱 초기화 + pip install이 완료되기 전에 첫 probe가 실행됐다.

### 해결

`start_period: 15s`로 넉넉하게 설정하고,
`interval: 10s`, `retries: 5`로 충분한 재시도 여유를 두었다.

healthcheck command를 `python -c "import urllib.request; urllib.request.urlopen(...)"` 로
Python stdlib만으로 구현해서, curl이 없는 slim 이미지에서도 동작하게 했다.

### 교훈

healthcheck의 timing 파라미터는 "가장 느린 환경"을 기준으로 설정해야 한다.
CI 러너처럼 리소스가 제한된 환경에서는 로컬보다 훨씬 느리다.

## 문제 2: lru_cache와 테스트 격리

### 증상

한 테스트에서 `DATABASE_URL`을 monkeypatch로 바꿨는데,
다른 테스트에서 이전 설정이 캐시에 남아서 잘못된 URL을 사용했다.

### 원인

`get_settings`에 `@lru_cache`가 걸려 있어서,
한 번 호출되면 같은 프로세스에서 계속 캐시된 인스턴스를 반환한다.
monkeypatch는 환경 변수를 바꾸지만 캐시는 건드리지 않는다.

### 해결

conftest에서 `get_settings.cache_clear()`를 fixture 시작/종료 시 호출한다.
이렇게 하면 매 테스트마다 새 Settings 인스턴스가 생성된다.

```python
@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    get_settings.cache_clear()
    with TestClient(create_app()) as c:
        yield c
    get_settings.cache_clear()
```

### 교훈

`lru_cache`와 테스트 격리는 충돌할 수 있다.
Settings 같은 환경 의존 객체에 lru_cache를 쓸 때는
반드시 cache_clear 전략을 함께 설계해야 한다.

## 문제 3: SQLite와 `SELECT 1` readiness check

### 증상

`/health/ready`에서 `db.execute(text("SELECT 1"))`이
PostgreSQL에서는 동작하지만, SQLite에서는 다른 에러 경로를 탔다.

### 원인

SQLite는 파일 기반이므로 "연결 실패"가 PostgreSQL과 다른 형태로 나타난다.
파일이 없으면 자동 생성되기도 한다.

### 해결

테스트 환경에서는 SQLite를 쓰되, readiness check의 `SELECT 1`은
SQLite에서도 정상 동작하므로 기본 케이스는 문제없다.
PostgreSQL 특유의 연결 실패 테스트는 integration/smoke 레벨에서만 검증한다.

### 교훈

readiness check는 DB 엔진에 따라 실패 양상이 다르다.
"SELECT 1이 성공하면 ready"라는 로직은
DB가 실제로 외부 서비스일 때만 의미가 있다.
