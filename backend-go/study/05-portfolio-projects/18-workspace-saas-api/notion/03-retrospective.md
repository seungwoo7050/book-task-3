# 회고 — 포트폴리오를 만든다는 것

## 학습 프로젝트와 포트폴리오 프로젝트의 차이

학습 프로젝트(01~17)는 "이 기술을 이해했는가?"를 증명한다. 포트폴리오 프로젝트는 "이 사람이 실무에서 일할 수 있는가?"를 증명한다.

차이는 코드의 복잡도가 아니라 **완결성**에 있다:
- OpenAPI 스펙이 있는가
- E2E 테스트가 있는가
- Docker Compose 한 번으로 재현 가능한가
- 에러 응답이 일관된 형식인가
- README가 5분 안에 실행 가능한 가이드인가

## 이전 프로젝트를 import하지 않은 이유

`internal/auth/tokens.go`는 프로젝트 07의 코드와 거의 동일하다. 하지만 go.mod에서 기존 프로젝트를 가리키지 않았다.

이유: 포트폴리오는 **독립 실행 가능한 단위**여야 한다. 면접관이 이 리포지토리만 클론해서 전체 동작을 확인할 수 있어야 한다. 외부 모듈 의존이 있으면 "다른 프로젝트도 있어야 동작합니다"라는 설명이 필요해진다.

## 두 바이너리 분리의 의미

`cmd/api`와 `cmd/worker`가 분리된 것은 아키텍처 결정이다:
- API는 수평 스케일 가능 (여러 인스턴스)
- Worker는 기본적으로 단일 인스턴스 (outbox 폴링 중복 방지)
- API 배포와 Worker 배포를 독립적으로 할 수 있음

Kubernetes에서 API는 Deployment + HPA, Worker는 Deployment (replicas: 1)로 배치하면 된다.

## Redis를 선택적 의존으로 만든 것

Redis가 없어도 서비스가 동작한다:
- 세션 검증: Redis miss → PostgreSQL fallback
- 대시보드: Redis miss → DB 직접 쿼리

이 설계 결정은 "Redis가 죽으면 서비스가 죽는" 상황을 방지한다. 단, 성능은 저하된다. `readyz`가 Redis 상태를 체크하므로 모니터링에서 감지 가능.

## Prometheus Text Format 직접 구현

`prometheus/client_golang` 라이브러리를 사용하지 않고 `atomic.Int64` + `fmt.Fprintf`로 직접 구현. 외부 의존성 최소화. 5개 카운터면 충분하고, histogram이나 summary가 불필요한 규모.

프로덕션에서는 `prometheus/client_golang`이 더 적절하지만, 포트폴리오에서는 "이 사람이 기본 원리를 이해하고 있다"는 것을 보여주는 것도 가치.

## 다음에 추가한다면

1. **Pagination**: 이슈, 댓글, 알림 목록에 cursor 기반 페이지네이션
2. **WebSocket**: 실시간 알림 (현재는 polling)
3. **Rate Limiting**: per-user/per-org 레벨 (현재는 없음)
4. **Audit Log**: 조직 내 모든 행위 기록
