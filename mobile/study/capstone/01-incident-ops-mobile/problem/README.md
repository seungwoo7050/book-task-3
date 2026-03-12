# Problem: Incident Ops Mobile Contract Harness

> Status: VERIFIED
> Scope: system contract capstone
> Last Checked: 2026-03-12

## 문제 요약

incident-ops backend와 shared DTO contract를 canonical source로 유지하고,
React Native harness가 그 계약을 올바르게 해석한다는 사실을 증명하는 capstone 과제다.

## 왜 이 문제가 커리큘럼에 필요한가

최종 앱을 만들기 전에 시스템 경계와 계약 자체를 먼저 증명해야 한다.
이 프로젝트는 "모바일 클라이언트가 제품 UX 없이도 contract correctness를 보여줄 수 있는가"를 확인한다.

## 제공 자료

- `problem/code/contracts/contracts.ts` shared DTO
- `node-server/` backend reference
- `react-native/` harness
- `problem/data/README.md` fixture 안내

## 필수 요구사항

1. login actor selection
2. incident list rendering
3. operator actions: `ack`, `request-resolution`
4. approver actions: `approve`, `reject`
5. audit timeline rendering
6. websocket replay diagnostics using `lastEventId`

## 의도적 비범위

- polished product UX
- persistent outbox
- portfolio packaging
- push/OTA infrastructure

## 평가/검증 기준

```bash
make test
make app-build
make app-test
make server-test
make demo-e2e
```

- contract package, harness, backend가 같은 모델을 설명해야 한다.
- demo 흐름이 재현 가능해야 한다.
- follow-up client 없이도 contract boundary를 이해할 수 있어야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
