# 04 Clustered KV Capstone

## 이 capstone을 어떻게 읽어야 하나

이 프로젝트는 "작은 분산 KV"라는 이름보다 더 구체적으로 읽어야 한다. 실제 소스는 앞선 세 랩에서 분리해 봤던 요소들을 한 요청 흐름 안으로 다시 묶는다. key는 shard ring으로 라우팅되고, shard leader는 disk-backed log에 append하며, follower는 watermark 이후 entry만 catch-up하고, node restart는 디스크 로그를 다시 읽어 state를 복원한다.

중요한 점은 이 통합이 networked cluster 완성본이 아니라는 것이다. topology는 정적이고 leader도 고정이며, replication은 in-process orchestration으로 수행된다. 그래서 이 capstone의 가치는 "실전 분산 KV를 다 만들었다"가 아니라 "routing, replication, storage를 한 코드 경로로 연결했다"는 데 있다.

이번 시리즈는 기존 blog를 입력으로 삼지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/problem/README.md), [`core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py), [`app.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/app.py), [`test_clustered_kv.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/tests/test_clustered_kv.py), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 끝까지 붙드는 질문

- write 요청은 어떤 순서로 shard, leader, follower, disk에 반영되는가
- follower catch-up은 어떤 watermark 규칙으로 작동하는가
- restart 뒤 state 복원은 정말 디스크에서 일어나는가
- HTTP surface가 드러내는 분산 경계와 감춰진 내부 경계는 무엇인가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/04-clustered-kv-capstone/10-chronology-scope-and-surface.md): capstone 범위와 route/write/read 표면을 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/04-clustered-kv-capstone/20-chronology-core-invariants.md): disk append, sequential offset, follower catch-up, restart reload invariant를 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/04-clustered-kv-capstone/30-chronology-verification-and-boundaries.md): pytest와 수동 재실행 결과를 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/04-clustered-kv-capstone/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/04-clustered-kv-capstone/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 capstone은 "정적 topology를 전제로 한 in-process distributed storage sketch"다. 그 덕분에 control plane 복잡도를 빼고도 distributed path와 disk path가 어떻게 접합되는지 선명하게 보여 준다. 반대로 dynamic membership, failover, consensus, remote transport는 아직 의도적으로 비워 둔다.

그리고 public FastAPI surface가 잠그는 읽기 경계도 더 좁다. HTTP `GET /kv/{key}`는 항상 leader-read 경로만 노출하고, stale follower 관찰은 `read_from_node()`를 직접 부르는 core-level 확인에서만 드러난다.
