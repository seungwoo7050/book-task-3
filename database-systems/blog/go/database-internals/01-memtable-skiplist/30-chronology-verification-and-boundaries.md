# Verification And Boundaries

## 1. 자동 검증은 MemTable contract를 거의 빠짐없이 잡는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/01-memtable-skiplist/tests	(cached)
```

테스트가 잡는 항목은 꽤 넓다.

- put/get 정상 경로
- missing key 상태
- update 뒤 logical size 유지
- 1000개 insert 뒤 lookup
- tombstone 상태와 tombstone 포함 size
- ordered entries
- tombstone이 iteration에서 유지되는지
- byte size tracking
- clear 뒤 완전 초기화

즉 이 랩은 작은 구현이지만 핵심 MemTable contract는 비교적 촘촘하게 검증된다.

## 2. demo 재실행이 문서에 준 추가 근거

demo 출력은 아래였다.

```text
ordered entries:
- apple => green
- banana => <tombstone>
- carrot => orange
size=3 byteSize=220
```

이 출력 덕분에 문서는 테스트 assert만 나열하지 않고, 삭제가 실제 ordered scan에서 어떻게 보이는지까지 설명할 수 있게 됐다. 특히 tombstone이 스캔 결과에 그대로 남는다는 점이 중요하다. 이후 SSTable flush나 compaction이 delete intent를 공유하려면 바로 이 ordered view가 필요하기 때문이다.

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 production-grade concurrent skip list로 읽으면 안 된다.

- lock이나 CAS가 없다
- iterator invalidation과 concurrent mutation safety가 없다
- benchmark나 level distribution measurement가 없다
- flush 자체는 구현하지 않는다
- range tombstone이나 versioned value도 없다

즉 지금 단계는 ordered MemTable contract를 고정하는 데 집중한다.

## 4. 보조 확인에서 드러난 환경 경계

이번에 프로젝트 밖 임시 Go 파일로 추가 snippet을 돌리려 했을 때 `internal` 패키지 import 제한 때문에 실행이 막혔다. 이건 구현 결함이 아니라 Go가 `internal/` 패키지 접근을 모듈 경계로 제한하는 규칙 때문이다. 그래서 이번 문서는 소스, 기존 테스트, demo 출력으로 직접 확인된 사실만 근거로 삼았다.

## 5. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 피했다.

- "고성능 skip list를 완성했다"
- "LSM write path 전체를 구현했다"
- "실전 수준의 메모리 사용량을 계산한다"

현재 소스가 실제로 보여 주는 것은 ordered entries, tombstone semantics, logical size와 byte-size estimate를 갖춘 학습용 MemTable이다. 그 범위를 벗어난 주장은 근거가 없다.
