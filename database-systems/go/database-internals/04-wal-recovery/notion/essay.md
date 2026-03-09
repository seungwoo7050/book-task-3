# 프로세스가 죽으면 MemTable은 사라진다 — WAL로 해결하기

## 이전 프로젝트에서 빠진 한 가지

03번에서 Mini LSM Store를 만들었다. Put, Get, Delete가 되고, flush가 되고, reopen도 된다.
하지만 한 가지 시나리오를 검증하지 않았다: **flush 전에 프로세스가 죽으면?**

MemTable은 메모리에만 존재한다. flush되지 않은 데이터는 프로세스 종료와 함께 증발한다.
사용자 입장에서는 "Put이 성공 응답을 줬는데 데이터가 없다"는 상황이 된다. acknowledged write loss.

해법은 고전적이다: **MemTable에 쓰기 전에, 먼저 디스크의 로그 파일에 기록해 둔다.** 이것이 Write-Ahead Log(WAL)이다.

## append-before-apply 원칙

이름 그대로다. "먼저 로그에 추가(append)하고, 그다음에 MemTable에 적용(apply)한다."

```
Put("key", "val") 호출
  └─ 1. WAL에 append   ← 디스크에 기록 (durable)
  └─ 2. MemTable에 put  ← 메모리에 기록 (volatile)
```

1번이 성공하면 acknowledge한다. 그 뒤 프로세스가 죽어도, 다음 Open 시 WAL을 replay하면 MemTable을 복원할 수 있다.

이 프로젝트의 `DurableStore`는 03번의 `LSMStore`에 WAL을 통합한 버전이다. `Put`과 `Delete` 메서드의 첫 줄이 `writeAheadLog.AppendPut()`과 `writeAheadLog.AppendDelete()`로 시작한다.

## WAL 레코드 포맷

WAL 파일은 append-only 바이너리다. 각 레코드는 다음 형태를 갖는다:

```
[CRC32: 4B][Type: 1B][KeyLen: 4B][ValLen: 4B][Key][Value]
```

- **CRC32** (4바이트): `[Type][KeyLen][ValLen][Key][Value]` 전체(payload)에 대한 체크섬. 손상 감지용.
- **Type** (1바이트): `0x01` = PUT, `0x02` = DELETE.
- **KeyLen** (4바이트): 키 바이트 길이 (big-endian).
- **ValLen** (4바이트): 값 바이트 길이 (big-endian). DELETE일 때는 `0xFFFFFFFF` (tombstone sentinel).
- **Key**: 키 바이트.
- **Value**: 값 바이트 (DELETE면 비어 있음).

이 포맷을 선택한 이유는 **self-describing** 구조이기 때문이다. 각 레코드가 자기 길이를 담고 있어서, 앞에서부터 순서대로 읽어나가면 레코드 경계를 알 수 있다. 그리고 CRC가 있으니까 corruption 여부도 레코드 단위로 판단할 수 있다.

## 복구 정책: 보수적으로 멈추기

WAL recovery는 파일을 처음부터 순서대로 읽어나간다. 그런데 중간에 손상된 레코드를 만나면 어떻게 할까?

이 프로젝트는 **"첫 손상 지점에서 멈추고, 그 뒤의 모든 레코드를 버린다"**는 보수적 정책을 택했다.

멈추는 조건은 세 가지:
1. **Truncated header**: 남은 바이트가 13바이트(헤더 크기)보다 적으면, 레코드 쓰기 중에 프로세스가 죽은 것으로 판단.
2. **Truncated payload**: 헤더는 읽었지만 key/value를 읽을 바이트가 부족하면, partial write.
3. **CRC mismatch**: 헤더는 온전한데 payload의 CRC가 맞지 않으면, bit corruption.

이 정책은 "손상 직전까지의 레코드는 신뢰하되, 그 이후는 일절 신뢰하지 않는다"는 원칙이다. 더 복잡한 전략(예: 손상 레코드만 건너뛰고 나머지를 살리기)도 있지만, 구현이 복잡해지고 정확성을 보장하기 어려워진다.

## flush 후 WAL rotation

MemTable이 flush되면 WAL은 어떻게 되는가?

1. 현재 WAL을 닫는다.
2. WAL 파일(`active.wal`)을 삭제한다.
3. 같은 경로에 새 빈 WAL을 연다.

이것이 WAL rotation이다. flush된 데이터는 이미 SSTable에 안전하게 기록됐으므로, WAL에 남아 있을 필요가 없다.
만약 WAL을 계속 남겨두면 recovery 시 이미 SSTable에 있는 데이터를 다시 replay하게 되고, WAL 파일도 계속 커진다.

## fsync라는 선택

WAL의 생성자에 `fsyncEnabled` 플래그가 있다. `true`면 매 레코드 append 후 `fsync()`를 호출한다.

`fsync()`는 OS 페이지 캐시의 내용을 물리적으로 디스크에 확정시키는 시스템 콜이다. 이게 없으면 OS가 쓰기를 버퍼링하다가, 정전 같은 상황에서 데이터가 날아갈 수 있다.

하지만 fsync는 느리다. 매 쓰기마다 호출하면 성능이 급격히 떨어진다.
이 프로젝트에서 테스트는 `fsyncEnabled=false`로 실행한다. 학습 목적에서는 fsync 여부보다 WAL의 logical correctness가 중요하기 때문이다.

## 테스트가 잡는 것

7개 테스트가 WAL과 DurableStore의 핵심 동작을 확인한다:

- **WAL 독립 테스트** (5개):
  - Put 레코드 기록 후 recover
  - Delete 레코드 기록 후 recover
  - 500개 대량 레코드 recover
  - 정상 레코드 뒤에 garbage 바이트를 append → 정상 레코드만 복구되는지
  - 존재하지 않는 WAL과 truncated WAL에서 빈 결과 반환

- **Store 통합 테스트** (2개):
  - Put → Close(flush 없이) → reopen → WAL에서 복구되는지
  - ForceFlush 후 WAL이 빈 상태로 rotation 되었는지, reopen 후 SSTable에서 읽히는지

## 돌아보며

WAL은 개념적으로는 단순하다 — "쓰기 전에 로그를 남긴다". 하지만 실제 구현에서는 의외의 지점들이 있었다.

CRC를 payload의 어느 범위에 걸 것인가, 레코드 중간에 잘린 파일을 어떻게 탐지할 것인가, flush 후 WAL을 어떻게 정리할 것인가. 이런 세부사항이 "durability guarantee"의 실체라는 걸 체감했다.

다음 프로젝트(05-leveled-compaction)에서는 쌓여가는 SSTable을 정리하는 compaction을 다룬다. WAL이 "쓰기를 안전하게 만드는" 장치라면, compaction은 "읽기와 공간을 효율적으로 만드는" 장치다.
