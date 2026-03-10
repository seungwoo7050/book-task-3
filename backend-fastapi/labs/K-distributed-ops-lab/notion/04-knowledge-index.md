# 지식 인덱스

## 먼저 적용할 판단 규칙

- live와 ready는 다른 질문에 답해야 한다.
- tracing backend가 없어도 request id와 JSON 로그는 먼저 남겨야 한다.
- target shape 문서는 “가정”과 “검증 완료”를 절대 섞지 않아야 한다.

## 핵심 개념과 사용 조건

### `live`

언제 보는가:
- 프로세스가 살아 있는지, 프로세스 수준에서 즉시 죽었는지를 알고 싶을 때

한계:
- live가 200이어도 DB, Redis, upstream dependency가 실제로 준비됐다는 뜻은 아니다.

이 랩의 근거:
- [../fastapi/gateway/app/api/v1/routes/health.py](../fastapi/gateway/app/api/v1/routes/health.py)
- [../fastapi/services/identity-service/app/api/v1/routes/health.py](../fastapi/services/identity-service/app/api/v1/routes/health.py)
- [../fastapi/services/workspace-service/app/api/v1/routes/health.py](../fastapi/services/workspace-service/app/api/v1/routes/health.py)
- [../fastapi/services/notification-service/app/api/v1/routes/health.py](../fastapi/services/notification-service/app/api/v1/routes/health.py)

### `ready`

언제 보는가:
- 요청을 받아도 되는지, dependency chain까지 포함해 확인하고 싶을 때

실패 징후:
- gateway는 살아 있는데 내부 서비스 하나만 내려가도 public readiness가 깨진다.
- health endpoint는 200인데 실제 user flow는 실패한다.

이 랩의 근거:
- [../fastapi/gateway/app/api/v1/routes/health.py](../fastapi/gateway/app/api/v1/routes/health.py)
- [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)
- [../fastapi/gateway/tests/integration/test_gateway_health.py](../fastapi/gateway/tests/integration/test_gateway_health.py)

### `JSON logging + request id`

왜 먼저 넣는가:
- 분산 구조에서 가장 싼 관측 수단이기 때문이다.
- tracing backend가 없어도 “이 요청이 어느 서비스까지 갔는가”를 최소한 추적할 수 있다.

이 랩의 근거:
- [../fastapi/gateway/app/core/logging.py](../fastapi/gateway/app/core/logging.py)
- [../fastapi/services/identity-service/app/core/logging.py](../fastapi/services/identity-service/app/core/logging.py)
- [../fastapi/services/workspace-service/app/core/logging.py](../fastapi/services/workspace-service/app/core/logging.py)
- [../fastapi/services/notification-service/app/core/logging.py](../fastapi/services/notification-service/app/core/logging.py)

### `target shape`

왜 문서만으로 남기는가:
- 이 랩의 목표는 실제 AWS 배포 완료가 아니라, 어떤 운영 구조를 상정하는지 설명하는 것이다.
- 학습 문서에서는 “배치 상정”과 “실제 배포 검증”을 분리할수록 가치가 커진다.

이 랩의 근거:
- [../docs/aws-deployment.md](../docs/aws-deployment.md)
- [../../../docs/verification-report.md](../../../docs/verification-report.md)

## 이 랩에서 제일 빨리 확인하는 순서

1. [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)에서 사용자 흐름 위에 health와 recovery가 어떻게 겹치는지 본다.
2. [../fastapi/gateway/app/api/v1/routes/health.py](../fastapi/gateway/app/api/v1/routes/health.py)에서 gateway가 own health와 upstream readiness를 어떻게 다루는지 본다.
3. [../fastapi/gateway/app/core/logging.py](../fastapi/gateway/app/core/logging.py)와 각 서비스 `core/logging.py`에서 JSON logging 필드 구성을 본다.
4. [../docs/aws-deployment.md](../docs/aws-deployment.md)에서 target shape가 어디까지 주장하고 어디서 멈추는지 확인한다.

## 실패 징후와 먼저 의심할 것

| 징후 | 먼저 의심할 것 | 이유 |
| --- | --- | --- |
| 컨테이너는 떠 있는데 사용자 요청은 계속 실패한다 | ready 기준 부족 | live만 보고 있다고 볼 수 있다 |
| 로그는 많지만 요청 흐름을 연결할 수 없다 | request id 부재 | 서비스별 로그가 분리된 채 남는다 |
| AWS 문서가 배포 완료처럼 읽힌다 | target shape 경계 붕괴 | 학습 문서와 검증 문서가 섞였다 |

## 참고 자료

- 제목: `labs/K-distributed-ops-lab/docs/aws-deployment.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: target shape 문서가 어디까지 주장하는지 다시 확인하기 위해 읽었다.
  - 배운 점: 학습 문서에서는 “상정하는 배치”와 “실제 검증된 배포”를 반드시 분리해야 한다.
  - 반영 결과: problem framing과 retrospective에 반영했다.
- 제목: `labs/K-distributed-ops-lab/fastapi/tests/test_system.py`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 운영성 랩에서 실제로 어떤 end-to-end 흐름을 재검증하는지 기록하기 위해 확인했다.
  - 배운 점: K 랩도 결국 도메인 흐름 위에서 health와 recovery를 설명해야 설득력이 생긴다.
  - 반영 결과: development timeline과 debug log에 반영했다.
