# 회고 — 16개 프로젝트의 귀결

## "알고 있다"와 "만들 수 있다"의 차이

프로젝트 14에서 멱등성 키를 구현했고, 프로젝트 15에서 Outbox를 구현했다. 캡스톤에서 둘을 합칠 때, "이미 아는 것"을 다시 구현하는 게 아니라 **조합하는 경험**을 한 것이다.

놀라운 점: 두 패턴을 합치면 복잡도가 2배가 아니라 3배가 된다. 멱등성 키와 Outbox 이벤트가 같은 트랜잭션에 있어야 하므로, 트랜잭션의 범위가 넓어지고 재시도 시 고려할 상태가 많아진다.

## Internal 패키지의 의미

`internal/`을 사용한 것은 단순한 관례가 아니다. Go의 컴파일러가 외부 모듈에서 `internal/` 하의 패키지를 import하는 것을 금지한다. 이 캡스톤은 독립 서비스이므로, 다른 서비스가 이 코드의 내부를 직접 사용하면 안 된다.

## 인터페이스 도입 시점

프로젝트 14에서 repository는 패키지 수준 함수였다. 캡스톤에서는 `Store` struct + 인터페이스로 바꿨다. 이유: relay가 `OutboxStore` 인터페이스에 의존하도록 해서 테스트에서 mock을 주입하기 위해.

인터페이스를 처음부터 정의한 게 아니라, 테스트가 필요해진 시점에 추출했다. Go에서는 인터페이스를 "사용하는 쪽"에서 정의하는 것이 관례.

## 에러 계층

서비스 에러를 HTTP 상태 코드로 매핑하는 패턴이 handler에 집중됐다:

```go
case errors.As(err, &validationErr):    → 400
case errors.Is(err, ErrPlayerNotFound): → 404
case errors.Is(err, ErrInsufficientBalance): → 409
case errors.Is(err, repository.ErrConflict): → 409
case errors.Is(err, ErrIdempotencyKeyConflict): → 409
default:                                → 500
```

서비스 레이어는 도메인 에러만 반환하고, HTTP 매핑은 handler의 책임. 이 분리 덕에 같은 service를 gRPC handler에서도 재사용할 수 있다 (프로젝트 12 참조).

## 캡스톤에서 빠진 것들

의도적으로 제외한 것들:
- 인증/인가 (프로젝트 07에서 별도로 다룸)
- Kafka Consumer (프로젝트 15에서 다룸)
- gRPC (프로젝트 12에서 다룸)
- Kubernetes 배포 (프로젝트 16에서 다룸)

캡스톤은 "모든 것을 넣는" 프로젝트가 아니라, **트랜잭션 일관성과 운영 기본**에 집중하는 프로젝트.

## 다시 만든다면

`QueryService`에 페이지네이션을 추가할 것이다. 현재 `GetPlayerInventory`는 전체 인벤토리를 반환하는데, 프로젝트 05에서 구현한 cursor 기반 페이지네이션을 적용하면 좋겠다.
