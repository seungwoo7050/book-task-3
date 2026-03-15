# workspace-backend-v2-msa Structure Plan

## 한 줄 초점
- v1의 public 협업 흐름을 유지한 채 내부를 MSA로 다시 풀었을 때 생기는 seam과 recovery 비용을 설명한다.

## 독자 질문
- public API는 그대로인데 왜 내부는 더 복잡해졌는가?
- gateway, DB ownership, outbox, stream receipt, recovery drain이 각각 어떤 비용을 추가하는가?

## 본문 구성
1. 비교 조건
   v1의 route shape를 유지한 채 왜 gateway가 먼저 필요해졌는지 설명한다.
2. 브라우저 경계
   쿠키와 CSRF가 gateway에만 남고 내부 서비스는 bearer claims만 읽는 구조를 본다.
3. DB ownership
   identity DB를 직접 읽지 못하는 workspace-service가 claims와 payload로만 협업 정보를 이어 가는 이유를 본다.
4. 이벤트 파이프라인
   comment -> outbox -> relay -> stream consume -> receipt dedupe -> pub/sub -> websocket fan-out을 따라간다.
5. recovery 시나리오
   notification-service 중단과 복구가 왜 주요 기능 검증이 되는지 설명한다.
6. 현재 검증 상태
   lint/test/smoke/system test가 현재 호스트에서 dependency 단계에서 막히는 사실을 닫는다.

## 반드시 연결할 증거
- `fastapi/gateway/app/main.py`
  request id, metrics, relay thread
- `fastapi/gateway/app/runtime.py`
  upstream 호출과 pub/sub -> websocket dispatch
- `fastapi/services/workspace-service/app/domain/services/platform.py`
  outbox 작성과 stream relay
- `fastapi/services/notification-service/app/domain/services/notifications.py`
  receipt dedupe와 delivered notification 저장
- `fastapi/tests/test_system.py`
  notification-service outage + recovery

## 서술 원칙
- 기존 blog 문장을 입력으로 삼지 않는다.
- v1보다 나아진 점만이 아니라 더 비싸진 점도 같이 적는다.
- target shape 문서와 실제 검증 결과를 섞지 않는다.
- 현재 canonical rerun 실패도 그대로 적는다.

## 이번 턴의 결론 문장
- `workspace-backend-v2-msa`는 v1의 기능 복제품이 아니라, 같은 public 흐름을 유지하려고 할 때 분산 구조가 어떤 추가 책임을 강제하는지 보여 주는 비교판이다.
