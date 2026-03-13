# 회고 — Realtime Collab Workspace

## 잘된 점

- transport를 mock과 browser용으로 분리해 데모와 테스트가 동시에 안정됐다.
- conflict banner, presence, activity log를 함께 둔 덕분에 sync 상태를 제품 언어로 설명하기 쉬워졌다.
- frontend-only 경계 안에서도 협업 UX의 핵심 tradeoff를 충분히 보여 줄 수 있었다.

## 아쉬운 점

- 현재 conflict는 "있다"를 보여 주는 수준이지 merge 해결 전략까지는 가지 않는다.
- text block은 whole-block overwrite라 rich text 협업과는 거리가 있다.
- auth, durable event log, cross-device sync가 없어서 제품 전체 그림은 일부러 잘라 두었다.

## 다음 확장 후보

1. durable event log와 reconnect snapshot
2. role-based editing permission
3. block-level text merge 또는 CRDT 입문 프로젝트 분리
