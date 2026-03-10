# 접근 로그

## 먼저 고정한 판단 기준

v2에서 중요한 것은 “서비스 수를 몇 개로 늘릴까”가 아니라, 같은 협업형 도메인을 다시 봤을 때 무엇을 분리 기준으로 삼느냐였다. 아래 기준을 먼저 고정했다.

- public contract를 누가 소유하는가
- 브라우저 상태를 어디서 끊어 낼 것인가
- DB ownership을 설명 가능한 수준으로 드러낼 수 있는가
- 알림 실패가 댓글 저장을 깨지 않게 만들 수 있는가
- v1과의 차이를 기능이 아니라 아키텍처로 설명할 수 있는가
- 로컬 Compose와 system test 비용이 학습 가치를 압도하지 않는가

## 처음 검토한 구조

1. `auth + platform + notifications` 세 서비스만 두고 gateway 없이 간다.
2. gateway를 두지만 `platform`은 하나의 큰 서비스로 남긴다.
3. `gateway + identity-service + workspace-service + notification-service`로 나누고, DB ownership도 함께 분리한다.

## 대안 비교 표

| 대안 | public contract 보존 | DB ownership 설명력 | 브라우저 상태 분리 | 장애 설명력 | 로컬 검증 비용 | 판단 |
| --- | --- | --- | --- | --- | --- | --- |
| `auth + platform + notifications` | 낮음 | 중간 | 낮음 | 중간 | 중간 | gateway가 없어서 v1 대비 차이가 흐려져 제외 |
| `gateway + platform + notifications` | 높음 | 낮음 | 높음 | 중간 | 중간 | `platform`이 너무 커서 v1과의 차이가 약해 제외 |
| `gateway + identity + workspace + notification` | 높음 | 높음 | 높음 | 높음 | 높음 | 채택 |

## 최종 선택

세 번째 구조를 채택했다. gateway는 public API shape와 브라우저 상태를 담당하고, `identity-service`는 토큰 발급과 회전을, `workspace-service`는 도메인 규칙과 outbox를, `notification-service`는 consumer와 pub/sub 발행을 맡는다.

## 그렇게 고른 이유

- gateway 없이 가면 public route shape를 유지하면서 internal contract를 바꾸는 의미가 약해진다.
- `platform`을 그대로 두면 v1과 v2 비교에서 가장 중요한 DB ownership 변화가 보이지 않는다.
- `notification-service`를 따로 빼야 “댓글 저장 성공”과 “알림 전달 성공”을 다른 사건으로 문서화할 수 있다.
- 네 서비스 구조는 가장 단순한 MSA는 아니지만, 경계 설명과 비교 학습에는 가장 적절하다.

## 채택 후 고정한 규칙

- 서비스 간 직접 DB 조회는 금지한다.
- 사용자 정보는 access token claims와 event payload만 넘긴다.
- comment 저장과 notification 전달은 분리하되, recovery 가능한 흐름으로 문서화한다.
- 브라우저 쿠키와 CSRF는 gateway에만 둔다.
- 외부 경로는 가능한 한 v1 public shape를 유지하고, 내부 경로만 `internal/*`로 바꾼다.

## 이 규칙이 실제로 드러나는 레포 근거

- gateway가 public contract를 소유하는 위치:
  - [../fastapi/gateway/app/api/v1/routes/auth.py](../fastapi/gateway/app/api/v1/routes/auth.py)
  - [../fastapi/gateway/app/api/v1/routes/platform.py](../fastapi/gateway/app/api/v1/routes/platform.py)
- request id를 edge에서 만들고 내부로 넘기는 위치:
  - [../fastapi/gateway/app/main.py](../fastapi/gateway/app/main.py)
  - [../fastapi/gateway/app/runtime.py](../fastapi/gateway/app/runtime.py)
- `workspace-service`가 자기 데이터와 outbox를 같이 다루는 위치:
  - [../fastapi/services/workspace-service/app/db/models/platform.py](../fastapi/services/workspace-service/app/db/models/platform.py)
  - [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)
- `notification-service`가 자기 DB만 쓰면서 dedupe 하는 위치:
  - [../fastapi/services/notification-service/app/db/models/notifications.py](../fastapi/services/notification-service/app/db/models/notifications.py)
  - [../fastapi/services/notification-service/app/domain/services/notifications.py](../fastapi/services/notification-service/app/domain/services/notifications.py)
- 이 선택이 실제로 어떤 사용자 흐름을 만들어 내는지 확인하는 테스트:
  - [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)

## 버린 대안이 특히 약했던 이유

### gateway 없이 가는 대안

- 외부 클라이언트가 여러 서비스 주소와 인증 계약을 직접 알아야 한다.
- 브라우저 쿠키와 내부 bearer 계약이 한 레벨에서 섞인다.
- v1과 달라진 점이 “서비스가 늘었다” 정도로만 보이고, public contract 재편이라는 설명이 약하다.

### `platform`을 큰 서비스로 남기는 대안

- gateway는 생기지만 DB ownership 변화는 거의 없다.
- invite, task, comment, outbox가 한 서비스 안에 남아 있어 “왜 여기서 서비스가 갈라졌는가”를 설명하기 어렵다.
- `identity-service`와 `workspace-service`의 계약을 claims 기준으로 줄이는 연습이 약해진다.

## 이 선택이 만든 비용

- 로컬 통합 테스트가 무거워졌다.
- 단순한 comment 알림 하나도 gateway, outbox, stream, consumer, pub/sub를 지나간다.
- 각 서비스의 env, health, cleanup까지 따로 챙겨야 한다.
- fresh build가 흔들리면 “서비스 코드 문제”와 “Docker 런타임 문제”를 먼저 분리해야 한다.

## 다시 판단해야 하는 신호

- `workspace-service`가 매 요청마다 사용자 profile 상세를 더 요구한다면 claim 계약이 너무 얇을 수 있다.
- gateway가 단순 proxy만 하고 오류 번역, 쿠키 경계, request id 전파 역할이 사라진다면 edge service로 둘 이유가 약해진다.
- `notification-service`가 workspace DB를 읽고 싶어지기 시작하면 event payload 설계가 약하거나 서비스 경계가 잘못 잘린 것이다.
- 로컬 검증 비용이 랩 설명력보다 커지면 서비스 수를 줄이는 편이 학습적으로 더 낫다.

## 지금 시점의 결론

이 구조는 “가장 운영 친화적인 구조”라서 선택한 것이 아니다. 같은 도메인을 기준으로 v1의 모듈 경계를 v2의 서비스 경계로 다시 드러내기에 가장 설명력이 높아서 선택했다. v2는 운영급 완성본이 아니라, 왜 이런 분산 구조가 생기고 어떤 비용이 따라오는지 정직하게 보여 주는 학습판이다.
