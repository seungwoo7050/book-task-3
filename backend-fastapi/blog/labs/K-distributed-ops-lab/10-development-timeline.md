# K-distributed-ops-lab 개발 타임라인

## 1. 이번 랩은 기능보다 운영 질문을 먼저 꺼냈다

`problem/README.md`를 읽으면 이번 랩의 주제가 바로 드러난다. MSA 구조를 실행만 하는 것으로 끝내지 않고, 서비스별 health, JSON 로그, 최소 metrics, target shape 문서를 함께 설명해야 한다. 그리고 AWS 문서는 실제 배포 완료처럼 쓰지 말아야 한다.

이 문제 정의는 꽤 중요했다. 왜냐하면 J 랩까지는 gateway와 이벤트 흐름이 중심이었고, K 랩은 그 위에서 "이 시스템이 지금 어떤 상태인지 어떻게 읽을 것인가"를 별도 학습 주제로 떼어냈기 때문이다. 같은 코드 베이스를 보더라도, 이번엔 기능 시나리오보다 운영 signal의 뜻을 먼저 읽어야 했다.

## 2. compose는 여전히 J와 비슷하지만, 읽는 관점이 달라졌다

`fastapi/compose.yaml`만 보면 구성은 J와 비슷하다. `gateway`, `identity-service`, `workspace-service`, `notification-service`, `redis`가 함께 올라오고, public entrypoint는 `8014`의 gateway다. 내부 서비스는 각각 `8131`, `8132`, `8133`, Redis는 `6394`를 쓴다.

하지만 이번 랩에서 중요한 건 이 토폴로지를 "누가 어떤 요청을 처리하나"가 아니라 "누가 어떤 상태 신호를 낼 수 있나"로 다시 읽는 것이다. 같은 다섯 컴포넌트라도, 운영 관점에서는 readiness 기준과 metrics 단위, 로그 상관관계가 더 핵심이 된다.

## 3. live와 ready는 서비스마다 다른 질문을 했다

가장 먼저 분명해진 것은 `/health/live`와 `/health/ready`가 이름은 같아도 같은 내용을 뜻하지 않는다는 점이다.

`identity-service/app/api/v1/routes/health.py`를 보면:

- `/live`는 단순히 `status="ok"`를 반환한다.
- `/ready`는 DB에 `SELECT 1`을 날려 인증 서비스의 저장소가 준비됐는지 확인한다.

`workspace-service`와 `notification-service`의 `health.py`는 한 단계 더 나간다.

- `/live`는 역시 단순한 process-level ok다.
- `/ready`는 DB `SELECT 1`뿐 아니라, `settings.redis_url`이 있으면 Redis `ping()`까지 확인한다.

즉, 이 둘은 "프로세스가 떠 있다"가 아니라 "이 서비스가 의존성까지 포함해 실제 기능을 수행할 수 있다"는 쪽에 더 가깝다.

그 다음 `gateway/app/api/v1/routes/health.py`를 보면 해석이 또 달라진다. gateway `/ready`는 자기 DB를 보지 않는다. 대신 내부 `identity`, `workspace`, `notification`의 `/health/ready`를 모두 호출하고, 필요하면 자체 Redis에도 `ping()`을 날린다. 따라서 gateway ready는 "gateway 프로세스 자체가 괜찮다"보다 "public edge 뒤의 전체 요청 경로가 준비됐다"는 집계 성격을 가진다.

이 차이를 분리해서 적는 것이 K 랩에서 가장 중요했다. 같은 `/ready`라는 이름을 써도, 내부 서비스와 gateway는 다른 질문에 답하고 있다.

## 4. metrics는 최소하지만, 서비스 경계를 읽기엔 충분했다

이번 랩의 metrics는 화려하지 않다. `gateway`, `identity-service`, `workspace-service`, `notification-service`의 `ops.py`를 보면 모두 거의 같은 형태로 `app_requests_total{service="..."}` 한 줄짜리 plaintext metrics를 제공한다.

예를 들면:

- gateway: `app_requests_total{service="gateway"}`
- identity-service: `app_requests_total{service="identity-service"}`
- workspace-service: `app_requests_total{service="workspace-service"}`
- notification-service: `app_requests_total{service="notification-service"}`

각 서비스의 `main.py` middleware도 요청이 들어올 때마다 `app.state.metrics.increment()`를 호출한다. 이건 정교한 관측 스택은 아니지만, 적어도 "어느 서비스에 요청이 얼마나 닿는가"를 서비스 경계 단위로 나눠 볼 수 있는 최소 기준선이다.

K 랩의 포인트는 바로 여기 있다. 분산 운영성을 처음 설명할 때부터 Prometheus histogram이나 tracing backend까지 바로 가지 않고, 가장 작은 signal을 서비스별로 먼저 고정한다.

## 5. JSON 로그는 service와 request_id를 최소 공통어로 삼았다

로그 쪽에서는 `core/logging.py`들이 더 흥미로웠다. gateway와 각 내부 서비스의 formatter는 공통적으로 JSON payload에 다음 필드를 넣는다.

- `timestamp`
- `level`
- `logger`
- `service`
- `request_id`
- `message`

`configure_logging(service_name)`는 context variable로 서비스 이름을 고정하고, `set_request_id()`/`reset_request_id()`는 요청 단위 상관관계를 유지한다. 각 서비스 `main.py` middleware는 요청 헤더의 `X-Request-ID`를 읽거나 새로 만들고, 응답 헤더에도 같은 값을 넣는다.

이 구성은 tracing backend나 log shipping은 아니지만, 적어도 "이 요청이 어느 서비스 로그에 남았는가"를 잇는 최소 연결고리로는 충분하다. 문제 정의가 굳이 request id와 JSON 로그를 분리해서 언급한 이유도 여기서 자연스럽게 읽힌다.

## 6. 테스트는 ops surface가 존재함을 최소한으로 확인했다

integration test들을 보면 ops 관점 확인도 꽤 간단하게 잡고 있다.

- `gateway/tests/integration/test_gateway_health.py`
- `notification-service/tests/integration/test_notification_service.py`

둘 다 `/api/v1/health/live`와 `/api/v1/ops/metrics`가 200인지 확인한다. 아주 깊은 검증은 아니지만, 적어도 운영 endpoint가 실제로 열려 있다는 최소 사실은 테스트로 고정한다.

중요한 건 여기서 테스트가 멈추는 지점이다. 현재 integration test는 metrics 본문이 어떤 값을 내는지, `request_id`가 로그 JSON payload에 실제로 박히는지, response header와 log context가 끝까지 일치하는지까지는 보지 않는다.

`tests/test_system.py`도 마찬가지다. recovery flow에서 `wait_for("http://127.0.0.1:8133/api/v1/health/ready")`로 notification-service 재기동을 기다리고 public 시나리오를 끝까지 밟지만, 로그 라인을 파싱하거나 metrics counter 증가량을 scrape하지는 않는다. 그래서 readiness의 세부 의미, request id correlation, metrics 집계 범위는 여전히 테스트와 함께 소스를 읽어야 정확해진다.

## 7. AWS 문서는 의도적으로 "가정 문서" 선을 넘지 않았다

`docs/aws-deployment.md`는 이번 랩에서 특히 조심해서 읽어야 하는 문서였다. 여기에는 ALB, ECS Fargate, RDS PostgreSQL, ElastiCache for Redis, Secrets Manager 같은 target shape가 정리돼 있다. 하지만 문서가 반복해서 말하는 건 이것이 실제 배포 완료 보고서가 아니라는 점이다.

이 문서는 다음을 보장하지 않는다고 분명히 적고 있다.

- 실제 AWS 계정에서의 실행 성공
- IaC 코드 존재
- 비용, 보안, 성능 최적화 검증

이건 사소하지 않다. 운영성 문서는 쉽게 "우리는 이렇게 배포한다"는 말투로 과장되기 쉽다. K 랩은 오히려 그 선을 분명히 그어서, 실행된 사실과 target shape 가정을 분리하는 연습까지 같이 시킨다.

## 8. system flow는 여전히 살아 있지만, 이번엔 운영 signal의 맥락에서 읽어야 했다

`tests/test_system.py`는 J 랩과 거의 같은 end-to-end 흐름을 유지한다. gateway를 통해 register, verify, login, workspace, invite, websocket notification, notification-service 중지/복구, recovery drain까지 밟는다.

이번 랩에서 중요한 건 이 시나리오 자체보다, 이런 복구 흐름을 읽을 때 어떤 운영 signal이 따라붙는가였다.

- gateway ready는 upstream 집계 준비 상태를 뜻한다.
- 각 서비스는 자기 `request_id`를 응답 헤더와 로그 문맥에 남긴다.
- metrics surface는 이런 요청들의 누적 흔적을 서비스별로 나눠 본다.
- AWS 문서는 이런 구성을 클라우드에 옮길 때의 "형태"만 설명한다.

즉, 같은 system test라도 K 랩에서는 "기능 성공"보다 "어떤 관측 신호와 함께 읽어야 하는가"가 더 핵심이다. 다만 이번 자동 검증이 직접 잠근 것은 health surface availability와 recovery path까지이고, observability payload의 세부 의미는 코드 해석이 남긴 몫이라는 선은 함께 그어야 한다.

## 9. 검증 결과는 이번에도 두 층으로 갈렸다

명령은 다시 직접 돌려 확인했다.

`make lint`는 통과했다. 정적 검사 기준에서 gateway와 내부 서비스, tests는 모두 깨지지 않았다.

반면 `make test`는 통과하지 못했다. gateway health test처럼 단순한 import 경로도 공용 security 모듈을 타면서 로컬 `python3` 환경의 `argon2` 누락에 막혔다. 따라서 실패 원인은 ops route 자체라기보다 host dependency 상태에 더 가깝다.

compose 기반 검증은 살아 있었다. `make smoke`는 통과했고, `python3 -m pytest tests/test_system.py -q`도 통과했다. 따라서 분산 구조가 올라와 public flow를 수행하고 복구 시나리오를 밟는다는 사실 자체는 최신 실행 결과로 확인됐다.

## 10. 이 랩을 지금 시점에서 어떻게 읽어야 하는가

K 랩은 "운영성을 넣었다"는 말만으로 읽으면 아쉽다. 실제로 더 정확한 요약은 이렇다.

- health는 서비스마다 다른 질문에 답한다.
- metrics는 단순하지만 서비스 경계 단위 신호를 준다.
- JSON 로그는 `service`와 `request_id`로 최소 correlation을 만든다.
- AWS 문서는 target shape일 뿐, 배포 성공 증거가 아니다.

좋은 운영 문서는 대시보드나 클라우드 용어를 많이 적는 문서가 아니라, 각 신호가 무엇을 말해 주고 무엇은 아직 말해 주지 못하는지를 정확히 적는 문서라는 점을 K 랩이 잘 보여 준다.
