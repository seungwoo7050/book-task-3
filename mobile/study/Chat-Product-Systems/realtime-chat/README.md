# Realtime Chat

Status: verified

## Summary

pending message, ack reconcile, replay, typing/presence 업데이트를 local-first 모델로 묶는 제품형 학습 과제다.

## Source Provenance

- Legacy source: `legacy/03-chat-product/realtime-chat`
- Study path: `study/Chat-Product-Systems/realtime-chat`

## Build/Test

```bash
make -C study/Chat-Product-Systems/realtime-chat/problem test
make -C study/Chat-Product-Systems/realtime-chat/problem app-build
make -C study/Chat-Product-Systems/realtime-chat/problem app-test
```
