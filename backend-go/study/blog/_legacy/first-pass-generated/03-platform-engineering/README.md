# 03 Platform Engineering blog

`03-platform-engineering`는 - 트랜잭션 재시도, outbox relay, GitOps 배포 자산을 각각 재현 가능한 프로젝트로 분리했다.

## 프로젝트 인덱스

| 프로젝트 | 시리즈 맵 | evidence ledger | structure | final blog | 대표 검증 |
| --- | --- | --- | --- | --- | --- |
| 14 Cockroach TX | [00-series-map](14-cockroach-tx/00-series-map.md) | [01-evidence-ledger](14-cockroach-tx/01-evidence-ledger.md) | [_structure-outline](14-cockroach-tx/_structure-outline.md) | [10-reconstructed](14-cockroach-tx/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -v ./service ./txn` |
| 15 Event Pipeline | [00-series-map](15-event-pipeline/00-series-map.md) | [01-evidence-ledger](15-event-pipeline/01-evidence-ledger.md) | [_structure-outline](15-event-pipeline/_structure-outline.md) | [10-reconstructed](15-event-pipeline/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -v ./outbox ./relay ./consumer` |
| 16 GitOps Deploy | [00-series-map](16-gitops-deploy/00-series-map.md) | [01-evidence-ledger](16-gitops-deploy/01-evidence-ledger.md) | [_structure-outline](16-gitops-deploy/_structure-outline.md) | [10-reconstructed](16-gitops-deploy/10-2026-03-13-reconstructed-development-log.md) | `make -C problem helm-lint` |
