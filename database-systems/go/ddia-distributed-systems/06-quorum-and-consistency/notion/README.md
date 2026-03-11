# 학습 노트 안내

replication 뒤에 바로 consensus로 넘어가면 consistency trade-off가 흐려지기 쉽기 때문에, 이 단계에서는 quorum read/write를 별도 register 실험으로 먼저 분리했습니다.

## 이 노트를 읽기 전에 잡을 질문
- read quorum과 write quorum은 왜 꼭 겹쳐야 하는가?
- stale read를 설명할 때 “replica 하나가 죽었다”보다 responder 집합을 먼저 봐야 하는 이유는 무엇인가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/quorum/quorum.go`, `../tests/quorum_test.go`, `../cmd/quorum-demo/main.go`를 열어 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 overlap과 stale read가 어떤 fixture로 재현되는지 확인합니다.
4. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 왜 replication 다음에 quorum consistency를 별도 단계로 두는지 정리합니다.
- `01-approach-log.md`: 결정적 responder 선택과 single-version register 같은 구현 선택을 기록합니다.
- `02-debug-log.md`: version이 잘못 전진하거나 read quorum이 불안정해질 때 어떤 징후가 보이는지 모아 둡니다.
- `03-retrospective.md`: consistency와 availability의 trade-off를 이 단계에서 무엇까지 설명했는지 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestReadReturnsLatestWhenQuorumsOverlap`, `TestStaleReadAppearsWhenQuorumsDoNotOverlap`, `TestWriteFailureDoesNotAdvanceVersion`, `TestReplicaFailuresReduceAvailability`
- 데모 경로: `../cmd/quorum-demo/main.go`
- 개념 문서: `../docs/concepts/quorum-read-write.md`, `../docs/concepts/versioned-register.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
