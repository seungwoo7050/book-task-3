# 회고: 운영을 부록이 아니라 기술로 다루기

## 잘된 것

**Liveness와 Readiness를 분리한 의미를 체감했다.**
live는 "프로세스가 살아있는가", ready는 "요청을 받을 준비가 되었는가".
이 구분이 Kubernetes에서 왜 중요한지, 분리하지 않으면 어떤
문제가 생기는지를 코드 수준에서 설명할 수 있게 되었다.

**JSON logging을 직접 구현했다.**
`logging.Formatter`를 상속해서 JSON을 출력하는 코드는 10줄도 안 되지만,
"왜 JSON 로그인가"에 대해 확실하게 답할 수 있게 되었다.
로그 수집기가 파싱할 수 있느냐 없느냐의 차이다.

**MetricsRegistry를 직접 만들었다.**
Prometheus client를 쓰기 전에 카운터가 내부적으로 어떻게 동작하는지
직접 만들어 봤으므로, 라이브러리를 쓸 때도 black box가 아니다.

**Compose healthcheck가 실제로 probing한다.**
README의 명령이 "돌아간다고 적혀 있다"가 아니라
CI에서 실제로 검증된다는 것이 신뢰도의 차이다.

## 아쉬운 것

**observability는 최소 수준이다.**
request count 하나만 있다. latency histogram, error rate,
그리고 무엇보다 tracing이 없다.
프로덕션 수준의 관찰 가능성과는 거리가 있다.

**AWS는 문서 중심이다.**
ECS, RDS, ElastiCache에 대한 노트는 있지만,
실제 deploy를 증명하지는 않는다.

**alert rule과 dashboard가 없다.**
metrics를 노출하는 것까지가 이 랩의 범위이고,
그 metrics를 보고 판단하는 도구는 다루지 않았다.

## 면접에서 쓸 수 있는 것

- liveness vs readiness probe의 차이와 Kubernetes에서의 역할
- structured logging의 필요성: 사람 vs 기계가 읽는 로그
- Compose healthcheck의 timing 파라미터 설계
- 자체 MetricsRegistry → Prometheus client 이행 경로
- lru_cache와 테스트 격리의 충돌과 해결
- 에러 응답 포맷 통일이 운영에 주는 이점
