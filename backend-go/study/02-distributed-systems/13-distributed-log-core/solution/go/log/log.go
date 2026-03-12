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

// Log는 여러 세그먼트를 묶어 단일 append-only 로그처럼 다룬다.
// 새 레코드는 항상 활성 세그먼트에 추가되고, 가득 차면 다음 세그먼트가 생성된다.
type Log struct {
	mu            sync.RWMutex
	dir           string
	config        Config
	segments      []*segment
	activeSegment *segment
}

// NewLog는 로그 디렉터리를 열고 기존 세그먼트를 복구한다.
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

// setup은 디렉터리의 세그먼트 파일을 스캔해 로그 상태를 복원한다.
func (l *Log) setup() error {
	files, err := os.ReadDir(l.dir)
	if err != nil {
		return err
	}

	// 세그먼트 파일명에서 base offset을 수집한다.
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

	// base offset 순서대로 세그먼트를 복구한다.
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

	// 비어 있는 로그라면 첫 세그먼트를 만든다.
	if len(l.segments) == 0 {
		if err := l.newSegment(0); err != nil {
			return err
		}
	}

	return nil
}

// newSegment는 새 세그먼트를 만들고 활성 세그먼트로 설정한다.
func (l *Log) newSegment(off uint64) error {
	seg, err := newSegment(l.dir, off, l.config)
	if err != nil {
		return err
	}
	l.segments = append(l.segments, seg)
	l.activeSegment = seg
	return nil
}

// Append는 활성 세그먼트에 레코드를 추가하고 절대 오프셋을 반환한다.
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

// Read는 지정한 절대 오프셋의 레코드를 읽는다.
func (l *Log) Read(off uint64) ([]byte, error) {
	l.mu.RLock()
	defer l.mu.RUnlock()

	// 요청한 오프셋을 포함하는 세그먼트를 찾는다.
	seg := l.findSegment(off)
	if seg == nil {
		return nil, fmt.Errorf("%w: %d", ErrOffsetOutOfRange, off)
	}
	return seg.Read(off)
}

// findSegment는 오프셋을 포함하는 세그먼트를 이진 탐색으로 찾는다.
// 호출자는 l.mu를 잡고 있어야 한다.
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

// LowestOffset은 현재 로그에 남아 있는 가장 작은 오프셋을 반환한다.
func (l *Log) LowestOffset() uint64 {
	l.mu.RLock()
	defer l.mu.RUnlock()
	return l.segments[0].baseOffset
}

// HighestOffset은 현재 로그에서 가장 큰 오프셋을 반환한다.
func (l *Log) HighestOffset() uint64 {
	l.mu.RLock()
	defer l.mu.RUnlock()
	off := l.activeSegment.nextOffset
	if off == 0 {
		return 0
	}
	return off - 1
}

// Truncate는 lowest 이전 데이터만 담고 있는 세그먼트를 제거한다.
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

// Close는 모든 세그먼트를 순서대로 닫는다.
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

// Reset은 로그를 비우고 초기 상태로 다시 만든다.
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
