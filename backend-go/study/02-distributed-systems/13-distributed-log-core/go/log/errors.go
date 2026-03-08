package log

import "errors"

var (
	// ErrIndexFull is returned when the index file has no room for another entry.
	ErrIndexFull = errors.New("index: file is full")
	// ErrIndexEmpty is returned when reading from an empty index.
	ErrIndexEmpty = errors.New("index: is empty")
	// ErrIndexOutOfRange is returned when the requested entry exceeds the index.
	ErrIndexOutOfRange = errors.New("index: entry out of range")
	// ErrSegmentFull is returned when a segment's store exceeds its max bytes.
	ErrSegmentFull = errors.New("segment: is full")
	// ErrOffsetOutOfRange is returned when reading a non-existent offset.
	ErrOffsetOutOfRange = errors.New("log: offset out of range")
)
