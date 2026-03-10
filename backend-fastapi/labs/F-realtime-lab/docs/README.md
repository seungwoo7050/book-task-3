# F-realtime-lab 문서 지도

이 문서는 실시간 연결과 presence 상태를 REST API와 다른 문제로 나눠 설명할 때 참고하는 개념 지도입니다.

## 먼저 보면 좋은 질문

- WebSocket 인증은 어디서 끝나야 하는가
- presence는 왜 TTL과 heartbeat를 함께 써야 하는가
- fan-out을 메모리에서 시작하고 Redis로 확장하는 경계는 어디인가

## 읽고 나면 설명할 수 있어야 하는 것

- 연결 상태와 사용자 상태의 차이
- 다중 연결 fan-out 모델
- reconnect를 고려한 보조 HTTP surface의 역할

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
