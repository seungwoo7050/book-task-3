# Realtime Chat

Status: verified

## 한 줄 답

offline send, ack reconcile, replay, typing/presence 업데이트를 하나의 local-first message model로 묶은 제품형 학습 프로젝트다.

## 무슨 문제를 풀었나

실시간 채팅은 네트워크, 로컬 상태, 소켓 재연결이 동시에 얽힌다.
이 프로젝트의 질문은 "pending message와 server event replay를 중복 없이 처리하면서도 사용자가 이해 가능한 모델을 만들 수 있는가"다.

## 내가 만든 답

- pending message 생성과 server ack reconcile을 구현했다.
- `lastEventId` 기반 replay와 dedupe를 추가했다.
- typing/presence 업데이트를 동일 모델 안에 넣었다.
- local storage schema와 제품 동작을 함께 문서화했다.

## 무엇이 동작하나

- offline send와 pending state
- ack 기반 message reconcile
- reconnect replay / dedupe
- typing / presence update
- local-first chat schema

## 검증 명령

```bash
make -C study/product-systems/02-realtime-chat/problem test
make -C study/product-systems/02-realtime-chat/problem app-build
make -C study/product-systems/02-realtime-chat/problem app-test
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- local-first 모델에서 메시지 생명주기를 어떻게 정의하는가
- replay와 dedupe를 제품 동작으로 설명하는 법
- 채팅 앱을 상태 머신 관점으로 읽는 법

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- 개념 문서: `verified`
