# F-realtime-lab 설계 문서

이 폴더는 F-realtime-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

- WebSocket 인증은 어디서 끝나야 하는가
- presence는 왜 TTL과 heartbeat를 함께 써야 하는가
- fan-out을 메모리에서 시작하고 Redis로 확장하는 경계는 어디인가

## 읽고 나면 설명할 수 있어야 하는 것

- 연결 상태와 사용자 상태의 차이
- 다중 연결 fan-out 모델
- reconnect를 고려한 보조 HTTP surface의 역할

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
