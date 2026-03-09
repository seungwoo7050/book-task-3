# 03-shard-routing — notion 폴더 가이드

이 폴더는 Shard Routing 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | Consistent Hash Ring과 Virtual Node 설계를 서사적으로 풀어낸 에세이 | "번호 하나 바뀌면 전부 옮겨야 하는" 단순 해시와의 차이를 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

Virtual node가 포함된 consistent hash ring으로 key를 물리 노드에 라우팅하고, 노드 추가/제거 시 최소한의 key만 재배치됨을 검증한다.

## 키워드

`consistent-hashing` · `virtual-node` · `hash-ring` · `shard-routing` · `rebalance` · `MurmurHash3` · `key-distribution` · `batch-routing`
