# 디버그 기록: WebSocket 테스트의 함정들

## 문제 1: WebSocket close code 검증 실패

### 증상

잘못된 token으로 연결했을 때 close code 1008을 기대했는데,
TestClient에서 code가 None으로 돌아왔다.

### 원인

Starlette의 `TestClient`가 WebSocket을 다루는 방식이
실제 클라이언트와 약간 다르다.
`ws.close(code=1008)`을 서버에서 호출하면,
테스트 클라이언트는 `WebSocketDisconnect` 예외를 받는데
close code 접근 방식이 버전마다 다르다.

### 해결

`with pytest.raises(WebSocketDisconnect)` 패턴으로 disconnection을 잡고,
`exc.code`에서 1008을 확인하는 방식으로 테스트를 작성했다.
Starlette 버전에 따라 동작이 다를 수 있으므로,
`httpx` 버전과 `starlette` 버전을 함께 고정했다.

### 교훈

WebSocket 테스트는 HTTP 테스트보다 프레임워크 내부 구현에 민감하다.
close code, disconnect 순서, async context 같은 부분에서
"실제 브라우저와 테스트 클라이언트의 차이"를 항상 의식해야 한다.

## 문제 2: Presence TTL 경계 조건

### 증상

`time.sleep(1.0)` 후에 online인 경우와 offline인 경우가 불안정하게 번갈아 나타났다.

### 원인

TTL이 정확히 1초일 때, sleep(1.0)은 경계값이다.
시스템 스케줄링에 따라 실제 경과 시간이 1.0초보다 약간 적을 수 있다.
`<` 비교에서 정확히 1.0이면 online으로 판정된다.

### 해결

테스트에서 `time.sleep(1.1)`로 여유를 두어 경계 불안정성을 해소했다.
TTL 비교는 `<` (strictly less than)으로 유지한다.

### 교훈

시간 기반 테스트에서 정확한 경계값(TTL = sleep duration)은 피해야 한다.
항상 여유 마진을 두거나, 시간을 목(mock)으로 대체하는 것이 안정적이다.

## 문제 3: ConnectionManager에서 빈 set 정리 누락

### 증상

사용자의 모든 WebSocket이 disconnect된 후에도
ConnectionManager에 빈 set이 남아 있어서
`send_to_user`가 빈 set을 순회하는 상황이 발생했다.

### 원인

`disconnect`에서 set.discard 후 empty 체크를 빠뜨렸다.

### 해결

`if not self._connections[user_id]: del self._connections[user_id]`를 추가했다.

### 교훈

컬렉션에서 원소를 제거한 뒤 빈 컨테이너를 정리하는 것은
메모리 누수 방지의 기본이다.
특히 장시간 실행되는 WebSocket 서버에서는 이런 누수가 누적된다.
