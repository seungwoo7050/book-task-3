package log

import (
	"fmt"
	"os"
	"path/filepath"
)

// Config는 세그먼트별 store/index 크기 제한을 정의한다.
type Config struct {
	MaxStoreBytes uint64
	MaxIndexBytes uint64
}

// segment는 하나의 store 파일과 index 파일을 묶어 관리한다.
// baseOffset부터 시작하는 연속된 레코드를 저장하며, 최대 크기에 도달하면 새 세그먼트로 넘긴다.
type segment struct {
	store      *store
	index      *index
	baseOffset uint64
	nextOffset uint64
	config     Config
}

// newSegment는 baseOffset 기준의 store/index 파일을 열고 세그먼트를 복구한다.
func newSegment(dir string, baseOffset uint64, c Config) (*segment, error) {
	storePath := filepath.Join(dir, fmt.Sprintf("%d.store", baseOffset))
	sf, err := os.OpenFile(storePath, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	if err != nil {
		return nil, err
	}
	st, err := newStore(sf)
	if err != nil {
		return nil, err
	}

	indexPath := filepath.Join(dir, fmt.Sprintf("%d.index", baseOffset))
	idxf, err := os.OpenFile(indexPath, os.O_RDWR|os.O_CREATE, 0644)
	if err != nil {
		return nil, err
	}
	idx, err := newIndex(idxf, c.MaxIndexBytes)
	if err != nil {
		return nil, err
	}

	seg := &segment{
		store:      st,
		index:      idx,
		baseOffset: baseOffset,
		nextOffset: baseOffset,
		config:     c,
	}

	// 재시작 상황이라면 마지막 엔트리를 읽어 다음 오프셋을 복원한다.
	if idx.Entries() > 0 {
		off, _, err := idx.Read(-1)
		if err != nil {
			return nil, err
		}
		seg.nextOffset = baseOffset + uint64(off) + 1
	}

	return seg, nil
}

// Append는 세그먼트에 레코드를 추가하고 절대 오프셋을 반환한다.
func (s *segment) Append(data []byte) (offset uint64, err error) {
	if s.store.Size() >= s.config.MaxStoreBytes {
		return 0, ErrSegmentFull
	}

	_, pos, err := s.store.Append(data)
	if err != nil {
		return 0, err
	}

	relOffset := uint32(s.nextOffset - s.baseOffset)
	if err := s.index.Write(relOffset, pos); err != nil {
		return 0, err
	}

	offset = s.nextOffset
	s.nextOffset++
	return offset, nil
}

// Read는 지정한 절대 오프셋의 레코드를 읽는다.
func (s *segment) Read(off uint64) ([]byte, error) {
	relOff := int64(off - s.baseOffset)
	_, pos, err := s.index.Read(relOff)
	if err != nil {
		return nil, err
	}
	return s.store.Read(pos)
}

// IsFull은 store 파일이 최대 크기에 도달했는지 보고한다.
func (s *segment) IsFull() bool {
	return s.store.Size() >= s.config.MaxStoreBytes
}

// Close는 index와 store를 차례대로 닫는다.
func (s *segment) Close() error {
	if err := s.index.Close(); err != nil {
		return err
	}
	return s.store.Close()
}

// Remove는 세그먼트를 닫고 관련 파일을 디스크에서 삭제한다.
func (s *segment) Remove() error {
	if err := s.Close(); err != nil {
		return err
	}
	if err := os.Remove(s.index.file.Name()); err != nil {
		return err
	}
	return os.Remove(s.store.file.Name())
}
