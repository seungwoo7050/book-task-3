# 디버그 로그

## 실패 사례

WebSocket 테스트에서 close code 검증이 불안정하거나, presence TTL 경계에서 online/offline 판정이 번갈아 흔들리는 문제가 있었다. 또 모든 연결이 끊긴 뒤에도 빈 connection set이 남는 경우가 있었다.

## 원인

- 테스트 클라이언트의 WebSocket 동작은 브라우저와 정확히 같지 않다.
- `sleep(1.0)` 같은 경계값 테스트는 시간 기반 로직을 불안정하게 만든다.
- disconnect 뒤 빈 컬렉션을 정리하지 않으면 상태 누수가 쌓인다.

## 수정

- disconnect는 예외와 close code를 함께 확인하는 방식으로 테스트했다.
- TTL 테스트는 경계값보다 조금 더 기다리도록 바꿨다.
- 마지막 연결이 끊기면 사용자별 connection set을 삭제하도록 정리했다.

## 검증 근거

- 이 실패는 실시간 테스트에서 경계값 시간과 disconnect 정리가 얼마나 민감한지 보여 준다.
- 마지막 기록된 검증 결과는 [../../../docs/verification-report.md](../../../docs/verification-report.md)를 따른다.
