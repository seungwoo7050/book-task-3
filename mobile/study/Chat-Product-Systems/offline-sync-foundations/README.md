# Offline Sync Foundations

Status: verified

## Summary

오프라인 create queue, retry, DLQ, idempotency, conflict merge를 채팅 앱 전에 분리 학습하는 브리지 프로젝트다.

## Source Provenance

- Legacy source: `study-designed project`
- Study path: `study/Chat-Product-Systems/offline-sync-foundations`

## Build/Test

```bash
make -C study/Chat-Product-Systems/offline-sync-foundations/problem test
make -C study/Chat-Product-Systems/offline-sync-foundations/problem app-build
make -C study/Chat-Product-Systems/offline-sync-foundations/problem app-test
```
