package log

import (
	"fmt"
	"os"
	"path/filepath"
)

// Config holds configuration for log components.
type Config struct {
	MaxStoreBytes uint64
	MaxIndexBytes uint64
}

// segment pairs a store and an index. It manages records whose offsets
// start at baseOffset. Once the store exceeds MaxStoreBytes, the segment
// is considered full.
type segment struct {
	store      *store
	index      *index
	baseOffset uint64
	nextOffset uint64
	config     Config
}

// newSegment creates a new segment for the given base offset in dir.
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

	// If the index already has entries (reopening), set nextOffset
	// based on the last indexed entry.
	if idx.Entries() > 0 {
		off, _, err := idx.Read(-1)
		if err != nil {
			return nil, err
		}
		seg.nextOffset = baseOffset + uint64(off) + 1
	}

	return seg, nil
}

// Append writes a record to the segment and returns the record's offset.
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

// Read returns the record at the given absolute offset.
func (s *segment) Read(off uint64) ([]byte, error) {
	relOff := int64(off - s.baseOffset)
	_, pos, err := s.index.Read(relOff)
	if err != nil {
		return nil, err
	}
	return s.store.Read(pos)
}

// IsFull returns true if the segment's store has reached its max size.
func (s *segment) IsFull() bool {
	return s.store.Size() >= s.config.MaxStoreBytes
}

// Close closes both the store and the index.
func (s *segment) Close() error {
	if err := s.index.Close(); err != nil {
		return err
	}
	return s.store.Close()
}

// Remove closes the segment and deletes its files from disk.
func (s *segment) Remove() error {
	if err := s.Close(); err != nil {
		return err
	}
	if err := os.Remove(s.index.file.Name()); err != nil {
		return err
	}
	return os.Remove(s.store.file.Name())
}
