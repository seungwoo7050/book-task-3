# MemTable 다음 질문: 디스크에는 어떻게 쓰는가

## SSTable이 필요한 이유

이전 프로젝트에서 MemTable을 SkipList로 구현했다. 메모리에서 키-값 쌍을 정렬된 상태로 유지하는 것까지는 됐다.
그런데 MemTable이 일정 크기를 넘으면 디스크로 내려야 한다. 이 "디스크에 내리는 행위"를 flush라고 부르는데, 그 결과물이 바로 SSTable(Sorted String Table)이다.

질문은 간단하다: **정렬된 키-값 레코드를 바이너리 파일 하나에 어떻게 담을 것인가?**

이 프로젝트는 SSTable 파일 포맷 자체에 집중한다. flush를 언제 할지, 어떻게 트리거할지는 다음 프로젝트(03-mini-lsm-store)의 영역이다.
여기서는 "파일을 쓰고, 닫고, 다시 열어서, 특정 키를 찾을 수 있는가"만 확인한다.

## 파일 하나의 해부학

SSTable 파일은 세 섹션으로 구성된다:

```
[ Data Section ][ Index Section ][ Footer (8 bytes) ]
```

**Data Section**: 레코드들이 키 오름차순으로 연속 배치된 영역이다. 각 레코드는 `[key_len: 4B][val_len: 4B][key][value]` 형태의 바이너리다. 여기서 `val_len`이 `0xFFFFFFFF`이면 tombstone이다 — 값이 없는 게 아니라 "이 키는 삭제됐다"는 마커인 셈이다.

**Index Section**: `(key, offset)` 쌍의 배열이다. "이 키는 Data Section의 바이트 오프셋 몇 번째에서 시작한다"를 기록한다. 나중에 point lookup 할 때 이 인덱스를 메모리에 올려서 이진 탐색한다.

**Footer**: 파일의 맨 마지막 8바이트. 앞 4바이트에 Data Section의 크기, 뒤 4바이트에 Index Section의 크기를 big-endian으로 적는다. 파일을 다시 열 때 뒤에서 8바이트를 읽으면 각 섹션의 경계를 바로 알 수 있다.

## 왜 footer가 파일 끝에 있는가

처음에는 header를 파일 앞에 두는 게 자연스럽다고 생각했다. 그런데 SSTable은 한 번 쓰고 나면 수정하지 않는(immutable) 파일이다.

파일 앞에 header를 두려면, Data Section을 다 쓸 때까지 전체 크기를 모른다. 그래서 모든 레코드를 쓴 다음에 파일 처음으로 돌아가서 크기를 갱신해야 한다. 반면 footer는 쓰기를 끝낸 뒤에 맨 끝에 append만 하면 된다. 한 방향으로만 쓰면 되니까 더 단순하다.

실제 LevelDB의 `.ldb` 파일 포맷도 footer를 파일 끝에 둔다. 같은 이유다.

## shared 패키지라는 설계 결정

이 프로젝트부터 `shared` 패키지를 사용하기 시작한다.

바이너리 직렬화(`serializer`)와 파일 I/O(`fileio`)는 SSTable뿐 아니라 이후 WAL, compaction, recovery에서도 동일하게 필요하다.  
매번 복사하는 대신 `go/shared/` 아래에 공용 패키지를 만들고, 각 프로젝트에서 `replace` 디렉티브로 참조한다:

```
require study.local/shared v0.0.0
replace study.local/shared => ../../shared
```

`serializer.Record`는 `Key string`과 `Value *string` 두 필드를 가진 구조체다. `Value`가 `nil`이면 tombstone이다. 이전 프로젝트의 SkipList `Entry`와 의도적으로 같은 계약을 유지한다.

## Lookup은 어떻게 동작하는가

SSTable을 다시 열었을 때의 조회 경로를 따라가 보자:

1. **Footer 읽기**: 파일 끝에서 8바이트를 읽어 Data Section과 Index Section의 크기를 파악한다.
2. **Index 적재**: Index Section의 시작 위치(= Data Section 크기)부터 Index Section 크기만큼 읽어서 디코딩한다. 결과는 `(key, offset)` 쌍의 슬라이스다.
3. **이진 탐색**: 찾으려는 키를 인덱스에서 이진 탐색한다. 인덱스가 정렬되어 있으므로 $O(\log n)$에 오프셋을 찾는다.
4. **레코드 읽기**: 찾은 오프셋에서 먼저 헤더 8바이트를 읽어 레코드 길이를 계산하고, 그 길이만큼 다시 읽어서 디코딩한다. 두 번 읽는 이유는 레코드 길이가 가변이기 때문이다.

여기서 중요한 점이 있다: malformed footer나 잘린 레코드를 만나면 조용히 넘기지 않고 에러를 반환한다.
"파일이 깨졌으면 최대한 빨리 알려주는 것"이 LSM-Tree 프로젝트 전체를 관통하는 원칙이다.

## tombstone이 바이너리에서도 보존되는 이유

01번 프로젝트에서 MemTable의 tombstone을 `nil` 포인터로 표현했다. SSTable에서도 같은 의미를 유지해야 한다.

만약 tombstone을 SSTable에 기록하지 않으면 어떻게 될까? 이전 레벨의 SSTable에 "key=foo, value=bar"가 남아 있다. 그런데 최신 MemTable에서 foo를 삭제했는데 그 기록이 flush 결과에 없다면, foo를 조회하면 삭제하기 전의 bar가 돌아온다. 유령 데이터가 되살아나는 것이다.

그래서 value length 자리에 `0xFFFFFFFF`라는 sentinel을 넣어서 "이건 삭제 마커"임을 명시한다. `uint32`의 최댓값이므로 정상적인 값 길이와 절대 겹치지 않는다.

## 테스트가 잡는 것

테스트는 6개 케이스로 구성된다:

- **Round-trip**: 3개 레코드를 쓰고, 새 인스턴스로 열어서 인덱스 로드 → Lookup이 되는지.
- **Missing key**: 없는 키를 찾으면 `found=false`인지.
- **Tombstone**: tombstone 레코드를 쓰고, Lookup 결과가 `found=true, value=nil`인지. `found=false`와 구분되어야 한다.
- **ReadAll**: Data Section 전체를 순차 디코딩해서 정렬 순서와 tombstone이 유지되는지.
- **Large dataset**: 1000개 레코드를 쓰고 중간 키를 찾아 인덱스 이진 탐색이 실제로 동작하는지.
- **Malformed footer**: 임의의 8바이트 파일을 만들어 LoadIndex가 에러를 반환하는지.

## 돌아보며

이 프로젝트를 마치고 나서가 체감이 온 지점은, **바이너리 포맷 설계가 곧 API 설계**라는 것이다.

Data Section의 레코드 배치 순서, Index Section의 위치 정보, Footer의 크기 기록 — 이 세 가지가 합의되면 Writer와 Reader가 서로 아무것도 공유하지 않아도 된다. 파일 하나가 계약서 역할을 한다.

다음 프로젝트(03-mini-lsm-store)에서 MemTable flush와 multi-SSTable 관리를 다룰 때, 이 포맷이 전제된다. SSTable 파일이 불변이고, 포맷이 고정되어 있으니까 compaction 같은 복잡한 연산도 "입력 SSTable을 읽고, merge해서, 새 SSTable을 쓴다"는 단순한 흐름으로 환원된다.
