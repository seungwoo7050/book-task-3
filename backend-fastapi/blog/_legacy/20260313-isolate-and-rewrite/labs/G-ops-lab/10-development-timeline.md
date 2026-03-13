# G-ops-lab 개발 타임라인

## 2026-03-09
### Session 1

- 목표: "운영성 랩"이라는 이름을 보고 처음엔 Prometheus + Grafana 전체 스택을 구축하는 건가 싶었다. `problem/README.md`를 읽어 실제 범위를 확인한다.
- 진행: 이 랩은 기능 API가 아니라 "이 백엔드가 살아 있는지, 준비됐는지, 몇 번 호출됐는지" 세 가지 질문에만 답하면 된다. observability 전체 스택이 아니라 최소 표면이다.
- 이슈: 처음엔 live와 ready가 무슨 차이인지 확실하지 않았다. 둘 다 "서버가 살아 있다"는 뜻 아닌가?
- 판단: live는 "프로세스가 응답 가능한가"(죽었으면 재시작해야 한다), ready는 "요청을 처리할 준비가 됐는가"(DB 연결 안 됐으면 트래픽을 보내면 안 된다). Kubernetes에서 이 구분이 실제로 쓰인다는 걸 나중에 확인했다.

CLI:

```bash
$ cd labs/G-ops-lab/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: health endpoint를 분리하고 metrics를 추가한다.
- 진행: live는 단순 200 응답, ready는 DB와 Redis 설정 상태를 체크해서 돌려준다.

```python
@router.get("/ready", response_model=dict)
def ready() -> dict[str, object]:
    settings = get_settings()
    return {
        "status": "ok",
        "checks": {
            "database": "configured" if settings.database_url else "missing",
            "redis": "configured" if settings.redis_url else "skipped",
        },
    }
```

처음엔 ready에서 실제 DB 연결 ping을 하려 했다. 하지만 이 랩은 최소 운영 표면을 보여 주는 것이 목적이므로, "설정이 있는가" 수준으로 충분하다. 실제 ping은 운영 환경에서 필요할 때 추가하면 된다.

- 이슈: metrics를 어떤 포맷으로 내보낼까? 처음엔 JSON으로 돌려보내려 했다.
- 조치: Prometheus가 기대하는 text 포맷(`# HELP`, `# TYPE`, 이름 값)을 흉내 내기로 했다. 이러면 나중에 실제 Prometheus가 scrape할 때 바로 연결된다.

```python
body = (
    "# HELP app_requests_total Total HTTP requests handled\n"
    "# TYPE app_requests_total counter\n"
    f"app_requests_total {registry.request_count}\n"
)
return Response(content=body, media_type="text/plain; version=0.0.4")
```

- 다음: 이 metrics가 실제로 증가하려면, 모든 요청을 세는 middleware가 필요하다.

### Session 3

- 목표: request counting middleware를 추가한다.
- 진행: middleware를 app 레벨에 붙여서 모든 HTTP 요청에 카운터를 올린다.

```python
@app.middleware("http")
async def count_requests(request: Request, call_next):
    app.state.metrics.increment()
    return await call_next(request)
```

처음엔 "이걸 route 안에서 해야 하나, middleware에서 해야 하나" 고민했다. route 안이면 endpoint마다 코드를 넣어야 하고 빠뜨릴 수도 있다. middleware면 모든 요청에 자동으로 적용된다.

- 이슈: metrics 요청 자체도 카운터를 올리나? 맞다. `/ops/metrics`를 호출해도 카운터가 올라간다. 처음엔 이걸 제외해야 하나 싶었는데, 이 랩에서는 "모든 HTTP 요청"을 센다는 단순함이 더 중요하다.
- 검증: 테스트가 live, ready, metrics 세 개를 한 번에 확인한다. 특히 metrics 응답에 `app_requests_total` 문자열이 포함되는지 검사.

CLI:

```bash
$ pytest tests/integration/test_ops.py -q
```

```
1 passed
```

### Session 4

- 목표: 전체 검증 루프를 돌리고, 이 랩이 `make smoke`와 Compose에서 특히 중요한 이유를 확인한다.
- 진행: 다른 랩은 기능 테스트가 핵심이지만, 이 랩은 "서버가 떴는가", "health가 응답하는가"가 핵심이므로 smoke와 Compose가 다른 랩보다 더 중요한 신호다.
- 검증: compile, lint, test, smoke, Compose live/ready probe 모두 통과.
- 다음: 이 랩까지가 필수 트랙(A~G)이다. 다음 단계인 workspace-backend capstone에서는 여기까지 쪼개 놓은 인증, 데이터, 비동기, 실시간, 운영성을 다시 한 백엔드로 합친다.

CLI:

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
```

```
1 passed
```

```bash
$ make smoke
$ docker compose up --build
$ curl http://localhost:8000/api/v1/health/live
```

```json
{"status": "ok"}
```

```bash
$ curl http://localhost:8000/api/v1/ops/metrics
```

```
# HELP app_requests_total Total HTTP requests handled
# TYPE app_requests_total counter
app_requests_total 2
```
