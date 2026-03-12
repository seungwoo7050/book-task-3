# Problem: Incident Ops Mobile Client

> Status: VERIFIED
> Scope: hiring-facing RN client + shared contract reuse
> Last Checked: 2026-03-12

## 문제 요약

기존 incident-ops domain과 shared contract를 유지한 채,
실제 화면 흐름, 오프라인 복구, replay-safe realtime behavior를 갖춘 hiring-facing RN 클라이언트를 완성하는 과제다.

## 왜 이 문제가 커리큘럼에 필요한가

system/contract harness만으로는 제품 완성도와 UX 판단을 설명할 수 없다.
이 프로젝트는 "같은 도메인을 유지하면서도 채용 제출용 수준의 앱으로 다시 구현할 수 있는가"를 최종적으로 묻는다.

## 제공 자료

- `capstone/01-incident-ops-mobile`의 shared contract
- `node-server/` local backend reference
- `problem/data/README.md` fixture 안내
- `problem/code/README.md`의 보조 자료

## 필수 요구사항

1. auth entry와 session restore
2. incident feed, detail, create form
3. role-based action flow
4. audit timeline
5. persistent outbox와 manual retry
6. websocket reconnect replay using `lastEventId`

## 의도적 비범위

- custom native module 작업
- OTA/update pipeline
- push infrastructure
- multi-tenant backend redesign

## 평가/검증 기준

```bash
make test
make app-build
make app-test
make server-test
make demo-e2e
```

- 다섯 명령이 모두 재현 가능해야 한다.
- RN client가 earlier harness와 독립된 완성작으로 설명돼야 한다.
- shared contract 재사용 사실이 README와 코드에서 확인돼야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
