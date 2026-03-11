# 부품 두 개를 조립해서 스토리지 엔진을 만들기

## SkipList와 SSTable, 그 다음은

01번에서 MemTable용 SkipList를 만들었다. 메모리에서 키-값 쌍을 정렬 상태로 유지하는 버퍼.
02번에서 SSTable 바이너리 포맷을 만들었다. 정렬된 레코드를 불변 파일로 쓰고, footer와 인덱스로 다시 찾는 구조.

이제 질문은 명확하다: **이 둘을 어떻게 연결해서 "Put, Get, Delete가 되는 스토리지 엔진"을 만드는가?**

이것이 LSM(Log-Structured Merge) Store의 최소 형태이다. 이 프로젝트에서는 compaction, WAL, 동시성 제어 없이 핵심 흐름만 조립한다.

## 쓰기 경로: 모든 것은 MemTable로 들어간다

`Put("key", "value")`를 호출하면, 값은 곧바로 디스크가 아니라 active MemTable(SkipList)에 들어간다.
이것이 LSM-Tree의 핵심 아이디어다 — **쓰기를 순차적 메모리 연산으로 바꿈으로써 쓰기 성능을 극대화**한다.

`Delete`도 마찬가지다. 실제로 뭔가를 지우는 게 아니라, MemTable에 tombstone을 삽입한다.

## flush: 메모리에서 디스크로 내리는 순간

MemTable은 영원히 커질 수 없다. `ByteSize()`가 threshold(기본 64KB)를 넘으면 flush가 발생한다.

flush의 절차는 이렇다:
1. 현재 active MemTable을 **immutable**로 전환한다. 이 시점부터 이 MemTable은 더 이상 쓰기를 받지 않는다.
2. 새로운 빈 MemTable이 즉시 active가 된다. 쓰기가 중단되지 않는다.
3. Immutable MemTable의 엔트리를 정렬 순서대로 꺼내서 SSTable로 쓴다.
4. SSTable이 디스크에 확정되면, SSTable 목록의 **맨 앞**(newest)에 등록한다.
5. Immutable MemTable 참조를 제거한다.

이 프로젝트에서 flush는 동기적이다. `Put` 호출 안에서 threshold를 넘으면 바로 flush가 실행된다. 실제 운영 시스템에서는 비동기로 하겠지만, 상태 분리의 패턴(active → immutable → disk)은 같다.

`ForceFlush()` 메서드도 있다. threshold에 관계없이 현재 MemTable을 디스크로 내린다. 테스트에서 특히 유용하다.

## 읽기 경로: newest-first 원칙

`Get("key")`는 어디서 값을 찾을까? 답은 "가장 최근에 쓴 곳부터 찾는다".

1. **Active MemTable** — 아직 flush되지 않은 최신 쓰기가 여기 있다.
2. **Immutable MemTable** — flush 진행 중이라면 여기도 확인한다.
3. **SSTable 목록 (newest → oldest)** — 가장 최근에 flush된 SSTable부터 순서대로.

어느 단계에서든 키를 찾으면 즉시 반환한다. 이것이 "newest-first" 원칙이다.

여기서 tombstone의 역할이 중요해진다. Active MemTable에서 키를 삭제했는데, 오래된 SSTable에 같은 키의 이전 값이 남아 있다면?
tombstone이 먼저 발견되므로 "삭제됨"으로 처리된다. tombstone이 없으면 과거의 값이 유령처럼 되살아난다.

## 내부 패키지 복사라는 선택

이 프로젝트의 `internal/` 디렉터리에는 `skiplist/`, `sstable/`, `lsmstore/` 세 패키지가 있다.
01번의 SkipList와 02번의 SSTable 코드를 **복사**해서 가져왔다. import로 참조하지 않았다.

이유는 단순하다: 각 프로젝트가 `go mod init`으로 독립된 모듈이므로, cross-module import는 workspace 설정에 의존하게 된다.
학습용 프로젝트에서 모듈 간 의존성을 만들면 "이 모듈을 먼저 빌드해야 저 모듈이 돌아간다"는 순서 제약이 생긴다.
`shared`는 범용 유틸리티라서 의존할 가치가 있지만, 이전 프로젝트의 도메인 코드는 복사해서 자급자족하는 편이 낫다고 판단했다.

## SSTable 파일 네이밍과 reopen

SSTable 파일명은 `000001.sst`, `000002.sst`, ... 형태로 순번이 증가한다.
`Open()` 시점에 디렉터리를 스캔해서 `.sst` 파일을 모두 찾고, 각각의 인덱스를 로드한다.
파일명에서 sequence 번호를 추출해 다음 번호를 결정한다.

이 흐름 덕분에 `Close()` → `Open()`을 해도 기존 데이터가 살아 있다.
`Close()` 시점에 `ForceFlush()`가 호출되어 MemTable에 남은 데이터도 디스크로 내린다.

## 테스트로 검증한 것

9개 테스트가 LSM Store의 핵심 계약을 확인한다:

- **기본 CRUD**: Put→Get, Missing, Update, Delete
- **자동 flush**: 작은 threshold(512B)에서 50개 키를 넣으면 SSTable이 생성되는지
- **ForceFlush 후 읽기**: flush 후에도 SSTable에서 값을 찾는지
- **MemTable 우선**: SSTable에 "old" 값이 있고 MemTable에 "new" 값이 있으면 "new"가 반환되는지
- **cross-level tombstone**: SSTable에 값이 있고, MemTable에 tombstone을 넣으면 삭제로 판정되는지
- **Persistence**: Close→reopen 후에도 데이터가 살아 있는지

## 돌아보며

이 프로젝트가 가르쳐준 것은 "LSM-Tree는 단순한 아이디어의 조합"이라는 점이다.
MemTable은 정렬된 쓰기 버퍼, SSTable은 불변 정렬 파일, 읽기는 newest-first 탐색. 이 세 가지만 조합하면 동작하는 스토리지 엔진이 된다.

하지만 빠진 것이 있다. 이 상태에서 프로세스가 죽으면 MemTable의 데이터가 날아간다. 다음 프로젝트(04-wal-recovery)에서 이 문제를 WAL로 해결한다.
