package log

import (
	"os"
	"syscall"
)

// indexEntryWidth는 단일 인덱스 엔트리의 크기다.
// 각 엔트리는 `[4바이트 상대 오프셋][8바이트 store 위치]`로 구성된다.
const indexEntryWidth = 12

// index는 메모리 매핑된 파일에 오프셋과 store 위치를 기록한다.
// 파일은 maxBytes까지 미리 확보해 두고, Close 시 실제 사용 크기로 줄인다.
type index struct {
	file *os.File
	mmap []byte
	size uint64 // 실제로 사용 중인 엔트리 바이트 수
	max  uint64 // 미리 확보한 최대 파일 크기
}

// newIndex는 파일을 메모리 매핑하고 최대 크기를 설정한다.
func newIndex(f *os.File, maxBytes uint64) (*index, error) {
	fi, err := os.Stat(f.Name())
	if err != nil {
		return nil, err
	}
	size := uint64(fi.Size())

	// mmap 전에 파일을 최대 크기까지 확장한다.
	if err := f.Truncate(int64(maxBytes)); err != nil {
		return nil, err
	}

	data, err := syscall.Mmap(
		int(f.Fd()),
		0,
		int(maxBytes),
		syscall.PROT_READ|syscall.PROT_WRITE,
		syscall.MAP_SHARED,
	)
	if err != nil {
		return nil, err
	}

	return &index{
		file: f,
		mmap: data,
		size: size,
		max:  maxBytes,
	}, nil
}

// Write는 상대 오프셋과 store 위치를 인덱스 끝에 추가한다.
func (idx *index) Write(off uint32, pos uint64) error {
	if idx.size+indexEntryWidth > idx.max {
		return ErrIndexFull
	}
	enc.PutUint32(idx.mmap[idx.size:idx.size+4], off)
	enc.PutUint64(idx.mmap[idx.size+4:idx.size+12], pos)
	idx.size += indexEntryWidth
	return nil
}

// Read는 지정한 엔트리 번호의 상대 오프셋과 store 위치를 반환한다.
// entry가 -1이면 마지막 엔트리를 읽는다.
func (idx *index) Read(entry int64) (off uint32, pos uint64, err error) {
	if idx.size == 0 {
		return 0, 0, ErrIndexEmpty
	}

	if entry == -1 {
		entry = int64(idx.size/indexEntryWidth) - 1
	}

	start := uint64(entry) * indexEntryWidth
	if start+indexEntryWidth > idx.size {
		return 0, 0, ErrIndexOutOfRange
	}

	off = enc.Uint32(idx.mmap[start : start+4])
	pos = enc.Uint64(idx.mmap[start+4 : start+12])
	return off, pos, nil
}

// Entries는 현재 인덱스에 기록된 엔트리 개수를 반환한다.
func (idx *index) Entries() uint64 {
	return idx.size / indexEntryWidth
}

// Close는 메모리 매핑을 해제하고 파일을 실제 사용 크기로 정리한 뒤 닫는다.
func (idx *index) Close() error {
	// 매핑을 해제하기 전에 파일 내용을 디스크에 반영한다.
	if err := idx.file.Sync(); err != nil {
		return err
	}
	// 메모리 매핑을 해제한다.
	if err := syscall.Munmap(idx.mmap); err != nil {
		return err
	}
	// 남는 미할당 공간을 제거한다.
	if err := idx.file.Truncate(int64(idx.size)); err != nil {
		return err
	}
	return idx.file.Close()
}
