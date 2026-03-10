# 지식 인덱스

## 먼저 적용할 판단 규칙

- gateway는 클라이언트 편의 장치라기보다 public contract 보존 장치다.
- 브라우저 상태를 edge에만 남기면 내부 서비스 인증 계약이 단순해진다.
- tracing backend가 없어도 request id가 없으면 upstream 오류를 설명하기 어렵다.

## 핵심 개념과 사용 조건

### `edge gateway`

언제 쓰는가:
- 외부 경로는 유지하고 내부 경계만 바꾸고 싶을 때
- 쿠키, CSRF, access token cookie 같은 브라우저 상태를 한 곳에 묶고 싶을 때
- 여러 내부 서비스 호출을 하나의 public 요청으로 조합하고 싶을 때

실패 징후:
- 클라이언트가 내부 서비스 URL을 직접 알아야 한다.
- 내부 오류 코드가 외부 응답에 그대로 새어 나온다.

이 랩의 근거:
- [../fastapi/gateway/app/api/v1/routes/platform.py](../fastapi/gateway/app/api/v1/routes/platform.py)
- [../fastapi/gateway/app/api/v1/routes/auth.py](../fastapi/gateway/app/api/v1/routes/auth.py)

### `upstream error translation`

왜 필요한가:
- edge는 내부 서비스 예외를 그대로 보여 주는 곳이 아니라, 외부용 HTTP 의미로 번역하는 곳이기 때문이다.
- notification-service가 내려갔을 때 gateway에서 503으로 정리돼야 클라이언트 계약이 안정적이다.

이 랩의 근거:
- [../fastapi/gateway/app/runtime.py](../fastapi/gateway/app/runtime.py)
- [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)

### `request id`

언제 먼저 넣는가:
- gateway에서 시작된 요청이 identity, workspace, notification 어디까지 갔는지 추적해야 할 때

이 랩의 근거:
- [../fastapi/gateway/app/main.py](../fastapi/gateway/app/main.py)
- [../fastapi/services/identity-service/app/main.py](../fastapi/services/identity-service/app/main.py)
- [../fastapi/services/workspace-service/app/main.py](../fastapi/services/workspace-service/app/main.py)
- [../fastapi/services/notification-service/app/main.py](../fastapi/services/notification-service/app/main.py)

### `websocket edge`

왜 gateway에 두는가:
- 브라우저는 gateway만 알면 되고, 내부 pub/sub와 connection fan-out은 edge 뒤에 숨길 수 있다.
- websocket 연결 수명주기와 domain event 전달을 분리해서 설명할 수 있다.

이 랩의 근거:
- [../fastapi/gateway/app/runtime.py](../fastapi/gateway/app/runtime.py)
- [../fastapi/gateway/app/api/v1/routes/platform.py](../fastapi/gateway/app/api/v1/routes/platform.py)

## 이 랩에서 제일 빨리 확인하는 순서

1. [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)에서 login -> workspace -> websocket -> drain -> recovery 흐름을 본다.
2. [../fastapi/gateway/app/main.py](../fastapi/gateway/app/main.py)에서 request id를 어디서 생성하는지 본다.
3. [../fastapi/gateway/app/runtime.py](../fastapi/gateway/app/runtime.py)에서 upstream error translation과 websocket fan-out을 같이 본다.

## 실패 징후와 먼저 의심할 것

| 징후 | 먼저 의심할 것 | 이유 |
| --- | --- | --- |
| 내부 서비스 오류가 클라이언트에 그대로 노출된다 | upstream error translation | edge 역할이 약하다 |
| websocket은 붙었는데 알림 recovery 흐름이 설명되지 않는다 | gateway와 notification 분리 | 연결 관리와 이벤트 소비를 섞어 보고 있다 |
| gateway가 거의 모든 비즈니스 규칙을 알기 시작한다 | edge 비대화 | contract 보존을 넘어 domain owner처럼 커지고 있다 |

## 참고 자료

- 제목: `labs/J-edge-gateway-lab/fastapi/tests/test_system.py`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: gateway가 실제로 어떤 public 흐름을 증명하는지 기록하기 위해 확인했다.
  - 배운 점: login, workspace, websocket, notification drain, recovery 흐름을 한 시나리오로 묶는 것이 가장 설득력 있다.
  - 반영 결과: `05-development-timeline.md`와 debug log에 반영했다.
- 제목: `capstone/workspace-backend-v2-msa/fastapi/gateway/app/runtime.py`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: request id와 websocket fan-out 경로를 다시 설명하기 위해 읽었다.
  - 배운 점: gateway는 REST fan-out뿐 아니라 pub/sub subscriber 역할도 같이 가진다.
  - 반영 결과: problem framing과 회고 문서에 반영했다.
