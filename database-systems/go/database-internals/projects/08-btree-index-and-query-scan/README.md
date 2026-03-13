# 08 BTree Index And Query Scan

| 항목 | 내용 |
| --- | --- |
| 상태 | `verified` |
| 문제 질문 | single-table point lookup, range scan, rule-based index usage를 가장 작은 표면으로 어떻게 보여 줄 것인가 |
| 내가 만든 답 | B+Tree leaf split, linked-leaf range cursor, rule-based query executor를 갖춘 최소 secondary-index lab |
| 검증 | `GOWORK=off go test ./...`<br>`GOWORK=off go run ./cmd/btree-index-and-query-scan` |

## 문제를 어떻게 해석했나

`07-buffer-pool`이 page를 붙잡는 쪽이었다면, 이번 단계는 그 page 위에서 key order를 어떻게 유지할지 보는 쪽이다. 범위는 B+Tree insert/split, duplicate key lookup, linked-leaf range scan, 그리고 "언제 index를 타고 언제 full scan으로 내려갈지"를 고르는 rule-based planner까지로 제한했다.

## 공개 표면

- `problem/README.md`: 문제 경계와 성공 기준
- `cmd/btree-index-and-query-scan/main.go`: point lookup / range scan demo
- `internal/btreeindex`: B+Tree insert, split, lookup, range cursor
- `internal/queryscan`: row store와 rule-based query executor
- `docs/README.md`: split, cursor, planner 개념 메모
- `notion/README.md`: 작업 로그

## 구현 요약

- `BTreeIndex`: duplicate key를 row id list로 묶는 secondary index
- `RangeCursor`: linked leaf를 따라가며 key order를 유지하는 cursor
- `QueryScanExecutor`: indexed equality/range는 index로, 나머지는 full scan으로 계획하는 작은 planner

## 검증

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/btree-index-and-query-scan
```

## 다음 단계

이 프로젝트 다음에는 transaction visibility를 붙여 "같은 key의 여러 version 중 지금 어떤 값을 볼 수 있는가"를 다루는 [09-mvcc](../09-mvcc/README.md)로 넘어간다.
