package log

import (
	"os"
	"syscall"
)

// indexEntryWidth is the size of a single index entry in bytes.
// Each entry is: [4 bytes offset (uint32)][8 bytes position (uint64)]
const indexEntryWidth = 12

// index wraps an os.File with a memory-mapped region for fast
// random-access reads and sequential writes. The file is pre-allocated
// to maxBytes and truncated to the actual data size on Close.
type index struct {
	file *os.File
	mmap []byte
	size uint64 // current size of meaningful data
	max  uint64 // maximum size (pre-allocated)
}

// newIndex creates (or opens) an index backed by the given file.
// maxBytes determines the maximum size of the index file.
func newIndex(f *os.File, maxBytes uint64) (*index, error) {
	fi, err := os.Stat(f.Name())
	if err != nil {
		return nil, err
	}
	size := uint64(fi.Size())

	// Grow the file to maxBytes so mmap has enough space.
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

// Write appends an index entry: the record's offset within its segment
// and the byte position within the store file.
func (idx *index) Write(off uint32, pos uint64) error {
	if idx.size+indexEntryWidth > idx.max {
		return ErrIndexFull
	}
	enc.PutUint32(idx.mmap[idx.size:idx.size+4], off)
	enc.PutUint64(idx.mmap[idx.size+4:idx.size+12], pos)
	idx.size += indexEntryWidth
	return nil
}

// Read returns the offset and position stored at the given entry number
// (0-indexed). If entry is -1, it returns the last entry.
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

// Entries returns the number of entries currently in the index.
func (idx *index) Entries() uint64 {
	return idx.size / indexEntryWidth
}

// Close syncs the mmap, truncates the file to the actual data size,
// and closes the file.
func (idx *index) Close() error {
	// Sync the underlying file to disk before unmapping.
	if err := idx.file.Sync(); err != nil {
		return err
	}
	// Unmap.
	if err := syscall.Munmap(idx.mmap); err != nil {
		return err
	}
	// Truncate to actual size — remove the pre-allocated empty space.
	if err := idx.file.Truncate(int64(idx.size)); err != nil {
		return err
	}
	return idx.file.Close()
}
