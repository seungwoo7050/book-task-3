# Pending Map

동시에 여러 RPC를 보낼 수 있으므로 응답은 요청 순서와 다르게 도착할 수 있다. 그래서 client는 `correlation_id -> pending call` map을 유지한다.

response가 도착하면:

1. correlation id로 pending entry를 찾고
2. timeout timer를 해제하고
3. result 혹은 error를 caller에게 전달한 뒤
4. map에서 제거한다

connection close가 발생하면 남은 pending call 전부를 실패로 정리해야 메모리 누수와 영원한 대기를 막을 수 있다.
