# Incident Ops Mobile

Status: verified

## 한 줄 답

이 프로젝트는 최종 포트폴리오 앱이 아니라 DTO contract, Node backend, RN harness를 canonical source로 고정하는 system/contract capstone이다.

## 무슨 문제를 풀었나

capstone을 곧바로 polished app으로 만들면 계약과 시스템 경계가 흐려진다.
이 프로젝트의 질문은 "모바일 클라이언트가 shared DTO contract를 올바르게 해석한다는 사실을 작은 harness와 backend로 증명할 수 있는가"다.

## 내가 만든 답

- shared DTO contract를 `problem/code/contracts`에 유지했다.
- `node-server/`를 canonical backend reference로 뒀다.
- `react-native/`는 계약 해석을 빠르게 검증하는 harness 역할만 맡겼다.
- 데모와 테스트 명령을 contract 중심으로 재현 가능하게 만들었다.

## 무엇이 동작하나

- actor 선택 로그인
- incident list와 detail 해석
- operator/approver action
- audit timeline rendering
- websocket replay diagnostics

## 검증 명령

```bash
make -C study/capstone/01-incident-ops-mobile/problem test
make -C study/capstone/01-incident-ops-mobile/problem app-build
make -C study/capstone/01-incident-ops-mobile/problem app-test
make -C study/capstone/01-incident-ops-mobile/problem server-test
make -C study/capstone/01-incident-ops-mobile/problem demo-e2e
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [node-server/README.md](node-server/README.md)
4. [docs/README.md](docs/README.md)
5. [notion/README.md](notion/README.md)

## 학습 포인트

- product UX와 system contract 증명을 분리하는 이유
- DTO, backend, client harness의 경계를 canonical source로 두는 법
- capstone을 데모 가능한 계약 시스템으로 설명하는 법

## 현재 상태

- 문제 정의: `verified`
- RN harness: `verified`
- Node backend: `verified`
- 문서: `verified`
