# App Distribution

Status: verified

## Summary

`realtime-chat`의 verified snapshot을 복사해 Fastlane, GitHub Actions, env separation,
local release rehearsal까지 닫는 배포 리허설 프로젝트다.

## Source Provenance

- Legacy source: `legacy/03-chat-product/app-distribution`
- Snapshot base: `study/Chat-Product-Systems/realtime-chat`
- Study path: `study/Chat-Product-Systems/app-distribution`

## Build/Test

```bash
make -C study/Chat-Product-Systems/app-distribution/problem test
make -C study/Chat-Product-Systems/app-distribution/problem app-build
make -C study/Chat-Product-Systems/app-distribution/problem app-test
make -C study/Chat-Product-Systems/app-distribution/problem release-rehearsal
```

## Current Status

- problem scaffold: rewritten for modern RN release rehearsal
- react-native implementation: verified
- release rehearsal assets: verified
