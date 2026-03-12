package log

import "errors"

var (
	// ErrIndexFull은 인덱스 파일에 더 이상 엔트리를 쓸 수 없을 때 반환된다.
	ErrIndexFull = errors.New("index: file is full")
	// ErrIndexEmpty는 비어 있는 인덱스를 읽으려 할 때 반환된다.
	ErrIndexEmpty = errors.New("index: is empty")
	// ErrIndexOutOfRange는 존재하지 않는 인덱스 엔트리를 읽으려 할 때 반환된다.
	ErrIndexOutOfRange = errors.New("index: entry out of range")
	// ErrSegmentFull은 세그먼트가 최대 크기에 도달했을 때 반환된다.
	ErrSegmentFull = errors.New("segment: is full")
	// ErrOffsetOutOfRange는 존재하지 않는 로그 오프셋을 읽으려 할 때 반환된다.
	ErrOffsetOutOfRange = errors.New("log: offset out of range")
)
