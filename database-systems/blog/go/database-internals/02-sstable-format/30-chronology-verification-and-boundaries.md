# Verification And Boundaries

## 1. 자동 검증은 round trip, tombstone, malformed footer까지 잡는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/02-sstable-format/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- sorted record round trip
- missing key lookup
- tombstone lookup
- full `ReadAll()` 복원
- 1000 record dataset lookup
- malformed footer detection

작은 프로젝트이지만 포맷 경계와 reopen 경로를 거의 빠짐없이 건드린다.

## 2. demo 재실행은 lookup 결과 네 상태를 보여 준다

demo 출력은 아래와 같았다.

```text
alpha => 1
beta => 2
gamma => <tombstone>
missing => <missing>
```

이 출력 덕분에 문서는 `Lookup()`의 반환 shape를 추상적으로 설명하지 않고, 실제 사용자 눈에 어떻게 구분되는지까지 적을 수 있다. tombstone과 missing이 명확히 다른 결과라는 점이 특히 중요하다.

## 3. malformed footer 경계도 다시 확인했다

추가로 아래 명령을 다시 실행했다.

```bash
GOWORK=off go test ./tests -run TestMalformedFooter -v
```

출력은 아래였다.

```text
=== RUN   TestMalformedFooter
--- PASS: TestMalformedFooter (0.00s)
PASS
```

즉 임의 8바이트만 들어 있는 잘못된 파일은 정상 SSTable처럼 해석되지 않는다. 이 프로젝트는 footer mismatch를 조용히 넘기지 않고 에러 경계로 다룬다.

## 4. 현재 구현이 일부러 다루지 않는 것

이 랩을 production SSTable reader/writer로 읽으면 곤란하다.

- compression이 없다
- checksum이나 corruption recovery가 없다
- block cache와 prefetch가 없다
- range scan 최적화가 없다
- manifest, multi-level file set, compaction 연결이 없다

즉 지금 구현은 immutable file format의 최소 계약을 고정하는 데 집중한다.

## 5. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 피했다.

- "RocksDB 스타일 SSTable을 완성했다"
- "대용량 on-disk query path를 최적화했다"
- "corruption-safe storage engine을 구현했다"

현재 소스와 테스트가 보여 주는 것은 sorted write, reopen-safe index load, tombstone sentinel, malformed footer rejection까지다. 그보다 큰 주장은 근거가 없다.
