# Incident Ops Mobile Client

Status: verified

## Summary

기존 `incident-ops-mobile`의 문제 도메인과 서버 계약을 유지한 채,
React Native 개발 역량 증명용 완성작으로 다시 구성한 최종 과제다.
시스템/계약 중심 캡스톤과 채용 제출용 앱 완성작을 분리해 학습 구조를 보존한다.

## Source Provenance

- Legacy source: `legacy/04-capstone/mobile-product-capstone`
- Copied-from study project: `study/Incident-Ops-Capstone/incident-ops-mobile`
- Study path: `study/Incident-Ops-Capstone/incident-ops-mobile-client`

## Build/Test

```bash
make -C study/Incident-Ops-Capstone/incident-ops-mobile-client/problem test
make -C study/Incident-Ops-Capstone/incident-ops-mobile-client/problem app-build
make -C study/Incident-Ops-Capstone/incident-ops-mobile-client/problem app-test
make -C study/Incident-Ops-Capstone/incident-ops-mobile-client/problem server-test
make -C study/Incident-Ops-Capstone/incident-ops-mobile-client/problem demo-e2e
```

## Docs

- `docs/concepts/client-architecture.md`
- `docs/concepts/offline-queue-replay.md`
- `docs/concepts/testing-pyramid-demo-checklist.md`
- `docs/portfolio-presentation.md`

## Why This Exists

- 기존 `incident-ops-mobile`은 문제 정의, 계약, 서버 흐름 증명에 더 가깝다.
- 새 프로젝트는 동일 도메인을 유지하면서 RN 앱 구조, 오프라인 큐 UX, 테스트, 데모 재현성을 별도 과제로 완성한다.
- 기존 프로젝트를 대체하지 않고, 앞선 캡스톤 위에 쌓는 마지막 단계로 둔다.

## Current Status

- problem scaffold: verified
- react-native implementation: verified with JS/type/test, iOS simulator run, and Maestro capture flows
- node-server: verified against the shared contract and local demo flow
- docs migration: verified for public repo + portfolio presentation scope
