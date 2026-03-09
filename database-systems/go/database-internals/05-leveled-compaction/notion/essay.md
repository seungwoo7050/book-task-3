# SSTable이 계속 쌓이면 어떻게 되는가 — Leveled Compaction

## 문제: 끝없이 늘어나는 SSTable

03번에서 Mini LSM Store를 만들었을 때, flush가 일어날 때마다 새 SSTable 파일이 하나씩 생겼다.
읽기는 newest-first로 SSTable을 순회했다. SSTable이 10개면 최악의 경우 10번 디스크 읽기, 100개면 100번.

이것이 LSM-Tree의 근본적 trade-off다: **쓰기 성능을 위해 append-only로 만들었더니, 읽기가 점점 느려진다.**

Compaction은 이 문제의 해법이다. 여러 SSTable을 읽어서 하나로 합치고, 중복된 키는 최신 값만 남기고, 오래된 파일은 삭제한다.

## Level이라는 개념

이 프로젝트는 Leveled Compaction을 구현한다. SSTable을 "레벨"로 분류한다:

- **L0**: flush가 직접 생성하는 SSTable. 키 범위가 겹칠 수 있다.
- **L1**: L0의 SSTable들을 merge한 결과. 키 범위가 겹치지 않는다.
- **L2** (이 프로젝트에서는 비어 있음): L1의 다음 레벨.

L0에 SSTable이 일정 개수(기본 4개) 이상 쌓이면 compaction을 트리거한다.
L0의 모든 SSTable과 L1의 기존 SSTable을 합쳐서 새 L1 SSTable 하나를 만든다.

## k-way merge: 여러 정렬된 스트림을 합치기

Compaction의 핵심 연산은 k-way merge다. 여러 개의 정렬된 레코드 배열을 하나의 정렬된 배열로 합친다.

이 프로젝트의 구현은 pairwise merge 방식이다:
1. `sources[0]`(가장 최신)부터 시작해서
2. `sources[1]`과 merge, 그 결과를 `sources[2]`와 merge, ...
3. 같은 키가 나오면 더 앞(더 최신) 소스의 값을 택한다.

`mergeTwo` 함수가 핵심이다. 두 정렬 배열을 합치는 표준적인 투 포인터 알고리즘에, "같은 키면 newer(왼쪽) 우선"이라는 규칙을 추가한 것이다.

여기서 중요한 세부사항이 있다: **L0 파일 리스트는 flush 순서(oldest-first)로 쌓이므로, compaction 입력을 만들 때 reverse 해서 newest-first로 바꿔야 한다.** 이걸 빠뜨리면 오래된 값이 최신 값을 덮어쓰는 치명적 버그가 된다.

## tombstone은 언제 지워도 되는가

merge 과정에서 tombstone을 만나면 두 가지 선택이 있다:

1. **유지**: tombstone을 결과에 포함한다.
2. **제거**: tombstone과 그에 해당하는 이전 값을 결과에서 빼버린다.

정답은 "더 깊은 레벨에 같은 키의 이전 값이 남아 있을 수 있느냐"에 달려 있다.

L1 → L2 compaction이고 L2 아래에 아무것도 없다면, tombstone을 지워도 안전하다. 삭제 마커를 전파할 더 깊은 레벨이 없기 때문이다.
하지만 L2에 파일이 있다면, tombstone을 지우면 L2의 오래된 값이 되살아난다.

이 프로젝트에서는 `len(manager.Levels[2]) == 0`일 때만 tombstone을 제거한다.

## 메타데이터: manifest의 원자성

Compaction은 데이터 파일과 메타데이터를 동시에 바꾸는 작업이다.

새 SSTable만 만들고 manifest를 못 바꾸면? → Reader가 새 파일의 존재를 모른다.
manifest만 바꾸고 파일 교체가 실패하면? → 존재하지 않는 파일을 가리킨다.

이 프로젝트는 다음 순서를 따른다:
1. 새 SSTable을 디스크에 기록한다.
2. 메모리의 level map을 업데이트한다.
3. `MANIFEST` 파일을 **atomic write** (임시 파일에 쓰고 rename) 로 저장한다.
4. 이전 입력 파일을 삭제한다.

manifest는 JSON 형식으로, `levels` (레벨별 파일 목록)과 `nextSequence` (다음 SSTable 번호)를 담는다.
`fileio.AtomicWrite`는 임시 파일에 쓰고 `os.Rename`으로 교체하는 방식이라, 중간에 crash가 나도 manifest가 half-written 상태가 되지 않는다.

## 테스트로 확인한 것

4개 테스트:

- **k-way merge 우선순위**: 같은 키에 새 값과 오래된 값이 있을 때 새 것만 남는지
- **tombstone 제거**: deepest level에서 tombstone이 제거되는지
- **L0→L1 compaction 전체**: 4개 L0 SSTable을 compaction → 올바른 값 남는지, 오래된 파일 삭제되는지
- **manifest round-trip**: 저장 → 로드 → 동일한 level map과 sequence

## 돌아보며

Compaction을 직접 구현하면서 느낀 것은, **merge 자체보다 "무엇을 언제 지워도 되는가"가 더 어렵다**는 점이다.

tombstone 제거 조건, manifest 갱신 순서, 파일 삭제 타이밍 — 이런 것들이 데이터 무결성을 결정한다. merge 알고리즘은 표준적인 투 포인터에 불과하지만, 그 주변의 상태 관리가 compaction의 실체다.

다음 프로젝트(06-index-filter)에서는 SSTable 조회를 더 효율적으로 만드는 sparse index와 bloom filter를 다룬다.
