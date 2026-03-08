// Package log implements a simple commit log backed by the file system.
// The log is composed of segments, each containing a store (data) file and
// an index file. Records are length-prefixed binary blobs.
package log

import (
	"bufio"
	"encoding/binary"
	"os"
	"sync"
)

// enc is the encoding used for persisting record sizes and index entries.
var enc = binary.BigEndian

// lenWidth is the number of bytes used to store a record's length.
const lenWidth = 8

// store wraps an os.File and provides append-only writes with a buffered
// writer, plus random-access reads. Each record is stored as:
//
//	[8 bytes: length of data][data bytes]
type store struct {
	mu   sync.Mutex
	file *os.File
	buf  *bufio.Writer
	size uint64
}

// newStore creates a store for the given file, resuming at the current
// file size so that appends continue where they left off.
func newStore(f *os.File) (*store, error) {
	fi, err := os.Stat(f.Name())
	if err != nil {
		return nil, err
	}
	return &store{
		file: f,
		buf:  bufio.NewWriter(f),
		size: uint64(fi.Size()),
	}, nil
}

// Append writes data to the store. It returns the number of bytes written
// (including the length prefix) and the position where the record starts.
func (s *store) Append(data []byte) (n uint64, pos uint64, err error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	pos = s.size

	// Write the length prefix.
	if err = binary.Write(s.buf, enc, uint64(len(data))); err != nil {
		return 0, 0, err
	}

	// Write the data.
	nn, err := s.buf.Write(data)
	if err != nil {
		return 0, 0, err
	}

	nn += lenWidth
	s.size += uint64(nn)
	return uint64(nn), pos, nil
}

// Read returns the record stored at the given position.
func (s *store) Read(pos uint64) ([]byte, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Flush buffer so that any recent writes are available for reading.
	if err := s.buf.Flush(); err != nil {
		return nil, err
	}

	// Read the length prefix.
	lenBuf := make([]byte, lenWidth)
	if _, err := s.file.ReadAt(lenBuf, int64(pos)); err != nil {
		return nil, err
	}
	dataLen := enc.Uint64(lenBuf)

	// Read the record data.
	data := make([]byte, dataLen)
	if _, err := s.file.ReadAt(data, int64(pos+lenWidth)); err != nil {
		return nil, err
	}
	return data, nil
}

// ReadAt reads len(p) bytes from the store starting at byte offset off.
// It implements io.ReaderAt.
func (s *store) ReadAt(p []byte, off int64) (int, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if err := s.buf.Flush(); err != nil {
		return 0, err
	}
	return s.file.ReadAt(p, off)
}

// Close flushes the buffer and closes the underlying file.
func (s *store) Close() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if err := s.buf.Flush(); err != nil {
		return err
	}
	return s.file.Close()
}

// Size returns the current size of the store in bytes.
func (s *store) Size() uint64 {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.size
}
