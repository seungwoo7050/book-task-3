# Incident Ops Mobile

Status: verified

## Summary

이 프로젝트는 최종 포트폴리오 앱이 아니라 `system/contract capstone`이다.
`node-server`와 `problem/code/contracts`를 canonical source로 유지하고,
`react-native/`는 그 계약을 빠르게 점검하는 harness 역할만 맡는다.

## Source Provenance

- Legacy source: `legacy/04-capstone/mobile-product-capstone`
- Study path: `study/Incident-Ops-Capstone/incident-ops-mobile`
- Follow-up product client: `study/Incident-Ops-Capstone/incident-ops-mobile-client`

## Build/Test

```bash
make -C study/Incident-Ops-Capstone/incident-ops-mobile/problem test
make -C study/Incident-Ops-Capstone/incident-ops-mobile/problem app-build
make -C study/Incident-Ops-Capstone/incident-ops-mobile/problem app-test
make -C study/Incident-Ops-Capstone/incident-ops-mobile/problem server-test
make -C study/Incident-Ops-Capstone/incident-ops-mobile/problem demo-e2e
```

## Current Status

- problem scaffold: verified
- react-native harness: verified
- node-server contract backend: verified
- docs migration: verified

## Follow-up Project

- polished product UX, persistent outbox, and portfolio narrative continue in [incident-ops-mobile-client](../incident-ops-mobile-client/README.md)
