# 지식 인덱스 — 분산 로그 핵심 구축에서 다룬 개념들

## Commit Log (커밋 로그)

한 번 기록되면 수정하지 않는, append-only 데이터 구조. Kafka, NATS JetStream, 데이터베이스의 WAL(Write-Ahead Log)이 모두 커밋 로그 위에 세워져 있다. 이 프로젝트의 전체가 커밋 로그 하나를 구현하는 과정이다.

## Append-Only Storage

데이터를 항상 파일 끝에 추가하는 방식. 기존 데이터를 덮어쓰지 않으므로 쓰기 충돌이 없고, 순차 I/O라 디스크 성능이 극대화된다. `store.Append`에서 `s.buf.Write`로 데이터를 버퍼에 추가하고 `s.size`를 갱신하는 패턴.

## Memory-Mapped File (mmap)

파일의 내용을 프로세스의 가상 메모리에 직접 매핑하는 기법. `syscall.Mmap`으로 매핑하면, 메모리 읽기가 곧 파일 읽기가 된다. 페이지 캐시를 OS가 관리하므로 별도 캐싱 불필요. `index.go`에서 인덱스 검색에 사용.

## Length-Prefix Encoding (길이 접두사 인코딩)

가변 길이 메시지를 직렬화할 때, 메시지 앞에 길이를 고정 크기(여기선 8바이트 uint64)로 붙이는 방식. 수신 측은 먼저 8바이트를 읽어 메시지 크기를 알고, 그만큼 더 읽는다. `binary.BigEndian.PutUint64`과 `binary.BigEndian.Uint64`으로 구현.

## Big-Endian (빅 엔디언)

최상위 바이트를 먼저 저장하는 바이트 순서. 네트워크 프로토콜의 표준(네트워크 바이트 오더). Go의 `encoding/binary` 패키지에서 `binary.BigEndian`으로 사용. 바이너리 파일의 이식성을 위해 엔디안을 명시적으로 정하는 것이 중요하다.

## Segment Rotation (세그먼트 회전)

하나의 Segment가 용량 한계에 도달하면 새 Segment를 생성해 기록을 이어가는 방식. `log.Append`에서 `l.activeSegment.IsFull()` 체크 후 `l.newSegment`를 호출하는 패턴. Kafka의 `log.segment.bytes`, `log.roll.ms`에 대응.

## Binary Search for Segment Lookup

여러 Segment 중 특정 offset을 포함하는 Segment를 찾을 때 `sort.Search`(이진 탐색)를 사용. Segment 배열이 baseOffset 순으로 정렬되어 있으므로 O(log n)에 올바른 Segment를 찾는다.

## bufio.Writer

Go 표준 라이브러리의 버퍼링 Writer. `store.go`에서 매번 시스템 콜을 호출하는 대신 메모리 버퍼에 먼저 쓰고, 버퍼가 차면 한꺼번에 flush한다. 쓰기 성능을 크게 올리지만, 읽기 전에 flush를 잊으면 데이터가 안 보인다.

## Sentinel Error

`errors.New`로 패키지 수준 변수에 정의하는 고정 에러. `errors.Is`로 비교할 수 있다. `ErrIndexFull`, `ErrSegmentFull` 등 5개 정의. 에러 메시지 문자열 비교 대신 타입 안전한 에러 처리를 가능하게 한다.

## io.ReaderAt

임의의 위치(offset)에서 읽기를 지원하는 인터페이스. `store.ReadAt`에서 `s.file.ReadAt`을 호출. Sequential read만 하는 `io.Reader`와 달리, offset을 지정해 원하는 위치를 바로 읽을 수 있다.

## os.ReadDir + filepath.Ext

디렉토리 내 특정 확장자 파일만 골라 나열하는 패턴. `log.setup()`에서 `.store` 파일을 찾아 기존 Segment를 복원할 때 사용. 파일명의 숫자 부분이 baseOffset이 되어 Segment 순서를 결정한다.
