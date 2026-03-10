# 개발 타임라인

## 이 문서의 목적

- 실시간 랩을 다시 볼 때 HTTP와 WebSocket이 어떻게 짝을 이루는지 재현 가능한 순서로 적는다.
- 가장 확실한 자동 검증 경로와, 선택적으로 눈으로 볼 수 있는 수동 WebSocket 경로를 함께 적는다.

## 1. 시작 위치를 고정한다

```bash
cd labs/F-realtime-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
cp .env.example .env
```

- 이 랩은 `.env.example`을 복사해도 Compose 전용 host 이름으로 바뀌지 않는다.
- 기본 설정은 SQLite와 optional Redis를 사용하고, `PRESENCE_TTL_SECONDS=1`이 핵심이다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_realtime.py -q
make smoke
```

- 테스트는 WebSocket 연결, heartbeat 이후 presence가 `online=true`로 보이는지, HTTP notification이 socket으로 fan-out 되는지, 잘못된 token이 즉시 disconnect 되는지, TTL 만료 뒤 offline으로 내려가는지 확인한다.
- `make smoke`는 앱 부팅과 `/api/v1/health/live`만 확인한다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- 이 루프는 connection manager나 presence 계산 로직을 수정할 때 가장 빠르다.
- Redis 없이도 핵심 동작은 재현된다.

## 4. Compose로 Redis까지 포함한 shape를 본다

```bash
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8004/api/v1/health/live
curl http://127.0.0.1:8004/api/v1/health/ready
```

- Compose에서는 API가 `8004`, Redis가 `6381` 포트로 노출된다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 수동 실시간 흐름을 재현한다

가장 안정적인 재현은 테스트다. 눈으로 직접 보고 싶다면 `wscat` 같은 WebSocket 클라이언트를 하나 준비한다.

```bash
npx wscat -c "ws://127.0.0.1:8004/api/v1/realtime/ws/notifications/alice?token=alice"
```

다른 터미널에서 presence를 올리고 조회한다.

```bash
curl -X POST http://127.0.0.1:8004/api/v1/realtime/presence/heartbeat \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"alice"}'

curl http://127.0.0.1:8004/api/v1/realtime/presence/alice
```

- 두 번째 응답의 `online`이 `true`여야 한다.

이제 HTTP notification을 넣어서 socket으로 전달되는지 본다.

```bash
curl -X POST http://127.0.0.1:8004/api/v1/realtime/notifications \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"alice","message":"build complete"}'
```

- `wscat` 화면에 `{"message":"build complete"}`가 도착해야 한다.

잘못된 token은 즉시 끊겨야 한다.

```bash
npx wscat -c "ws://127.0.0.1:8004/api/v1/realtime/ws/notifications/bob?token=wrong"
```

presence TTL도 확인한다.

```bash
curl -X POST http://127.0.0.1:8004/api/v1/realtime/presence/heartbeat \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"carol"}'

sleep 2
curl http://127.0.0.1:8004/api/v1/realtime/presence/carol
```

- 마지막 응답의 `online`은 `false`여야 한다.

## 6. 막히면 먼저 확인할 것

- WebSocket이 붙지 않으면 URL path보다 query string의 `token`부터 다시 본다.
- presence가 안 내려가면 `.env`의 `PRESENCE_TTL_SECONDS`가 1인지 확인한다.
- 수동 WebSocket 클라이언트 준비가 번거롭다면 다시 `pytest tests/integration/test_realtime.py -q`로 돌아가는 것이 가장 빠르다.
