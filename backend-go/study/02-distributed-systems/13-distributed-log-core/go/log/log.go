package log

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"sync"
)

// Log manages a set of segments. Records are appended to the active
// (newest) segment. When the active segment is full, a new one is
// created. Old segments can be truncated.
type Log struct {
	mu            sync.RWMutex
	dir           string
	config        Config
	segments      []*segment
	activeSegment *segment
}

// NewLog creates or restores a Log in the given directory.
func NewLog(dir string, c Config) (*Log, error) {
	if c.MaxStoreBytes == 0 {
		c.MaxStoreBytes = 1024 * 1024 // 1 MB
	}
	if c.MaxIndexBytes == 0 {
		c.MaxIndexBytes = 1024 * 1024 // 1 MB
	}

	l := &Log{
		dir:    dir,
		config: c,
	}

	if err := l.setup(); err != nil {
		return nil, err
	}
	return l, nil
}

// setup scans the directory for existing segments and restores them,
// or creates a new initial segment.
func (l *Log) setup() error {
	files, err := os.ReadDir(l.dir)
	if err != nil {
		return err
	}

	// Collect unique base offsets from existing segment files.
	baseOffsets := map[uint64]struct{}{}
	for _, f := range files {
		name := f.Name()
		ext := filepath.Ext(name)
		if ext != ".store" && ext != ".index" {
			continue
		}
		base := strings.TrimSuffix(name, ext)
		off, err := strconv.ParseUint(base, 10, 64)
		if err != nil {
			continue
		}
		baseOffsets[off] = struct{}{}
	}

	// Sort and restore segments.
	var offsets []uint64
	for off := range baseOffsets {
		offsets = append(offsets, off)
	}
	sort.Slice(offsets, func(i, j int) bool { return offsets[i] < offsets[j] })

	for _, off := range offsets {
		if err := l.newSegment(off); err != nil {
			return err
		}
	}

	// If no existing segments, create the first one.
	if len(l.segments) == 0 {
		if err := l.newSegment(0); err != nil {
			return err
		}
	}

	return nil
}

// newSegment creates a new segment and makes it the active one.
func (l *Log) newSegment(off uint64) error {
	seg, err := newSegment(l.dir, off, l.config)
	if err != nil {
		return err
	}
	l.segments = append(l.segments, seg)
	l.activeSegment = seg
	return nil
}

// Append adds a record to the log and returns its offset.
func (l *Log) Append(data []byte) (uint64, error) {
	l.mu.Lock()
	defer l.mu.Unlock()

	if l.activeSegment.IsFull() {
		nextBase := l.activeSegment.nextOffset
		if err := l.newSegment(nextBase); err != nil {
			return 0, err
		}
	}

	off, err := l.activeSegment.Append(data)
	if err != nil {
		return 0, err
	}
	return off, nil
}

// Read returns the record stored at the given offset.
func (l *Log) Read(off uint64) ([]byte, error) {
	l.mu.RLock()
	defer l.mu.RUnlock()

	// Find the segment that contains this offset.
	seg := l.findSegment(off)
	if seg == nil {
		return nil, fmt.Errorf("%w: %d", ErrOffsetOutOfRange, off)
	}
	return seg.Read(off)
}

// findSegment performs a binary search on segments to find which one
// contains the given offset. Must be called with l.mu held.
func (l *Log) findSegment(off uint64) *segment {
	idx := sort.Search(len(l.segments), func(i int) bool {
		return l.segments[i].nextOffset > off
	})
	if idx >= len(l.segments) {
		return nil
	}
	seg := l.segments[idx]
	if off < seg.baseOffset {
		return nil
	}
	return seg
}

// LowestOffset returns the lowest offset in the log.
func (l *Log) LowestOffset() uint64 {
	l.mu.RLock()
	defer l.mu.RUnlock()
	return l.segments[0].baseOffset
}

// HighestOffset returns the highest offset in the log.
// Returns 0 if the log is empty.
func (l *Log) HighestOffset() uint64 {
	l.mu.RLock()
	defer l.mu.RUnlock()
	off := l.activeSegment.nextOffset
	if off == 0 {
		return 0
	}
	return off - 1
}

// Truncate removes all segments whose highest offset is below lowest.
func (l *Log) Truncate(lowest uint64) error {
	l.mu.Lock()
	defer l.mu.Unlock()

	var remaining []*segment
	for _, seg := range l.segments {
		if seg.nextOffset <= lowest {
			if err := seg.Remove(); err != nil {
				return err
			}
			continue
		}
		remaining = append(remaining, seg)
	}
	l.segments = remaining
	return nil
}

// Close closes all segments in the log.
func (l *Log) Close() error {
	l.mu.Lock()
	defer l.mu.Unlock()

	for _, seg := range l.segments {
		if err := seg.Close(); err != nil {
			return err
		}
	}
	return nil
}

// Reset closes the log, removes all files, and sets up a fresh log.
func (l *Log) Reset() error {
	if err := l.Close(); err != nil {
		return err
	}
	if err := os.RemoveAll(l.dir); err != nil {
		return err
	}
	if err := os.MkdirAll(l.dir, 0755); err != nil {
		return err
	}
	l.segments = nil
	l.activeSegment = nil
	return l.setup()
}
