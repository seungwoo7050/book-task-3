# Incident Ops Mobile Client

Status: verified

## 한 줄 답

`incident-ops-mobile`의 shared contract와 backend를 유지한 채, auth, feed, role action, persistent outbox, demo flow를 갖춘 hiring-facing RN 완성작으로 다시 구성한 최종 프로젝트다.

## 무슨 문제를 풀었나

system/contract capstone만으로는 제품 완성도와 사용자 경험을 설명하기 어렵다.
이 프로젝트의 질문은 "같은 incident domain을 유지하면서도 채용 제출용 RN 앱 수준의 완성도로 다시 구현할 수 있는가"다.

## 내가 만든 답

- 기존 contract와 backend reference를 그대로 재사용했다.
- auth entry, incident feed, create form, role action, audit timeline을 구현했다.
- persistent outbox, retry, replay-safe realtime behavior를 추가했다.
- demo 흐름과 portfolio 문서를 분리해 결과물을 설명 가능하게 만들었다.

## 무엇이 동작하나

- role selection / session restore
- incident list / detail / create flow
- operator / approver action
- persistent outbox와 manual retry
- websocket reconnect replay

## 검증 명령

```bash
make -C study/capstone/02-incident-ops-mobile-client/problem test
make -C study/capstone/02-incident-ops-mobile-client/problem app-build
make -C study/capstone/02-incident-ops-mobile-client/problem app-test
make -C study/capstone/02-incident-ops-mobile-client/problem server-test
make -C study/capstone/02-incident-ops-mobile-client/problem demo-e2e
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [node-server/README.md](node-server/README.md)
4. [docs/README.md](docs/README.md)
5. [notion/README.md](notion/README.md)

## 학습 포인트

- contract capstone 위에 제품 완성작을 쌓는 방법
- offline recovery와 demo reproducibility를 사용자 경험과 함께 설명하기
- hiring-facing 프로젝트를 과잉 서술 없이 요약하는 법

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- Node backend: `verified`
- portfolio 문서: `verified`
