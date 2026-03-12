// Package log는 파일 기반 분산 로그의 저장소 계층을 구현한다.
package log

import (
	"bufio"
	"encoding/binary"
	"os"
	"sync"
)

// enc는 길이와 오프셋을 직렬화할 때 사용하는 바이트 순서다.
var enc = binary.BigEndian

// lenWidth는 레코드 길이를 저장하는 바이트 수다.
const lenWidth = 8

// store는 길이 접두사가 붙은 레코드를 순차적으로 저장하는 파일 래퍼다.
// 각 레코드는 `[8바이트 길이][데이터 바이트]` 형식으로 기록된다.
type store struct {
	mu   sync.Mutex
	file *os.File
	buf  *bufio.Writer
	size uint64
}

// newStore는 기존 파일 크기를 기준으로 이어 쓰기 가능한 store를 만든다.
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

// Append는 현재 파일 끝에 레코드를 추가하고, 기록한 바이트 수와 시작 위치를 반환한다.
func (s *store) Append(data []byte) (n uint64, pos uint64, err error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	pos = s.size

	// 길이 접두사를 먼저 기록한다.
	if err = binary.Write(s.buf, enc, uint64(len(data))); err != nil {
		return 0, 0, err
	}

	// 실제 레코드 바이트를 이어서 기록한다.
	nn, err := s.buf.Write(data)
	if err != nil {
		return 0, 0, err
	}

	nn += lenWidth
	s.size += uint64(nn)
	return uint64(nn), pos, nil
}

// Read는 지정한 위치에 저장된 레코드를 읽어 반환한다.
func (s *store) Read(pos uint64) ([]byte, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// 가장 최근 쓰기까지 읽을 수 있도록 버퍼를 비운다.
	if err := s.buf.Flush(); err != nil {
		return nil, err
	}

	// 먼저 길이 접두사를 읽는다.
	lenBuf := make([]byte, lenWidth)
	if _, err := s.file.ReadAt(lenBuf, int64(pos)); err != nil {
		return nil, err
	}
	dataLen := enc.Uint64(lenBuf)

	// 길이만큼 레코드 본문을 읽는다.
	data := make([]byte, dataLen)
	if _, err := s.file.ReadAt(data, int64(pos+lenWidth)); err != nil {
		return nil, err
	}
	return data, nil
}

// ReadAt는 지정 오프셋에서 len(p) 바이트를 읽는다.
func (s *store) ReadAt(p []byte, off int64) (int, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if err := s.buf.Flush(); err != nil {
		return 0, err
	}
	return s.file.ReadAt(p, off)
}

// Close는 버퍼를 비우고 파일 핸들을 닫는다.
func (s *store) Close() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if err := s.buf.Flush(); err != nil {
		return err
	}
	return s.file.Close()
}

// Size는 현재까지 기록된 유효 바이트 수를 반환한다.
func (s *store) Size() uint64 {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.size
}
