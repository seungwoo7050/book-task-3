# 회고: 상태가 있는 서버의 다른 무게감

## 잘된 것

**WebSocket 생명주기를 직접 관리했다.**
connect/disconnect/send 각 단계를 ConnectionManager에서 명시적으로 다루니,
HTTP의 stateless 모델과 WebSocket의 stateful 모델이 어떻게 다른지
코드 수준에서 체감할 수 있었다.

**HTTP와 WebSocket의 협업 패턴을 구현했다.**
"HTTP POST로 메시지를 생성하고, WebSocket으로 실시간 전달한다"는 구조는
실제 서비스에서도 자주 쓰이는 패턴이다.
이 랩에서 그 흐름을 최소한으로 만들어 볼 수 있었다.

**Presence를 직접 추적했다.**
heartbeat + TTL 만료라는 단순한 구조지만, "온라인 상태란 무엇인가?"라는
질문에 구체적인 코드로 답할 수 있게 되었다.

**PostgreSQL 없이 돌아가는 경량 구조.**
이 랩은 의도적으로 DB를 뺐다.
모든 상태가 인메모리에 있으므로, 프로세스 재시작 시 모든 연결과 presence가 사라진다.
이것이 단점이 아니라 이 랩의 학습 포인트다—영속화가 필요한 시점을 인식하게 된다.

## 아쉬운 것

**스케일아웃 시나리오를 다루지 못했다.**
프로세스가 2개 이상이면 인메모리 ConnectionManager는 무용지물이다.
Redis pub/sub이나 메시지 브로커가 필요한데, 이 랩에서는 범위 밖이다.

**인증이 너무 약하다.**
`token == user_id`는 학습 편의를 위한 것이지만,
JWT 검증으로 바꿔야 실제 서비스에 가까워진다.

**presence TTL이 너무 짧다.**
1초 TTL은 테스트에서는 편하지만, 실제 시스템의 30~60초와는 거리가 있다.
heartbeat 주기와 TTL의 관계를 더 현실적으로 설정할 수 있었다.

## 면접에서 쓸 수 있는 것

- WebSocket과 HTTP의 근본적 차이: persistent connection vs request-response
- ConnectionManager 패턴: user_id → set[WebSocket] 구조와 disconnect 정리
- Presence 구현: heartbeat + TTL, 시간 기반 online 판정
- 인메모리 상태의 한계와 Redis pub/sub으로의 확장 방향
- WebSocket 인증: query param token의 한계와 JWT 대안
- 시간 기반 테ス트에서의 경계값 문제와 마진 전략
