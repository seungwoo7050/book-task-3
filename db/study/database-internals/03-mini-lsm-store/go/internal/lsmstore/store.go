package lsmstore

import (
	"path/filepath"
	"strconv"
	"strings"

	"study.local/database-internals/03-mini-lsm-store/internal/skiplist"
	"study.local/database-internals/03-mini-lsm-store/internal/sstable"
	"study.local/shared/fileio"
	"study.local/shared/serializer"
)

const DefaultMemtableThreshold = 64 * 1024

type LSMStore struct {
	DataDir               string
	MemtableSizeThreshold int
	Memtable              *skiplist.SkipList
	ImmutableMemtable     *skiplist.SkipList
	SSTables              []*sstable.SSTable
	nextSequence          int
}

func New(dataDir string, memtableSizeThreshold int) *LSMStore {
	if memtableSizeThreshold == 0 {
		memtableSizeThreshold = DefaultMemtableThreshold
	}
	return &LSMStore{
		DataDir:               dataDir,
		MemtableSizeThreshold: memtableSizeThreshold,
		Memtable:              skiplist.New(),
		nextSequence:          1,
	}
}

func (store *LSMStore) Open() error {
	if err := fileio.EnsureDir(store.DataDir); err != nil {
		return err
	}

	files, err := fileio.ListFiles(store.DataDir, ".sst")
	if err != nil {
		return err
	}

	store.SSTables = []*sstable.SSTable{}
	for _, fileName := range files {
		table := sstable.New(filepath.Join(store.DataDir, fileName))
		if err := table.LoadIndex(); err != nil {
			return err
		}
		store.SSTables = append(store.SSTables, table)

		var sequence int
		sequence, err := strconv.Atoi(strings.TrimSuffix(fileName, ".sst"))
		if err == nil && sequence >= store.nextSequence {
			store.nextSequence = sequence + 1
		}
	}

	reverseTables(store.SSTables)
	return nil
}

func (store *LSMStore) Put(key, value string) error {
	store.Memtable.Put(key, value)
	return store.maybeFlush()
}

func (store *LSMStore) Delete(key string) error {
	store.Memtable.Delete(key)
	return store.maybeFlush()
}

func (store *LSMStore) Get(key string) (*string, bool, error) {
	if value, state := store.Memtable.Get(key); state != skiplist.Missing {
		return value, true, nil
	}

	if store.ImmutableMemtable != nil {
		if value, state := store.ImmutableMemtable.Get(key); state != skiplist.Missing {
			return value, true, nil
		}
	}

	for _, table := range store.SSTables {
		value, found, err := table.Lookup(key)
		if err != nil {
			return nil, false, err
		}
		if found {
			return value, true, nil
		}
	}

	return nil, false, nil
}

func (store *LSMStore) ForceFlush() error {
	if store.Memtable.Size() == 0 {
		return nil
	}
	return store.flush()
}

func (store *LSMStore) Close() error {
	return store.ForceFlush()
}

func (store *LSMStore) maybeFlush() error {
	if store.Memtable.ByteSize() < store.MemtableSizeThreshold {
		return nil
	}
	return store.flush()
}

func (store *LSMStore) flush() error {
	store.ImmutableMemtable = store.Memtable
	store.Memtable = skiplist.New()

	records := make([]serializer.Record, 0, store.ImmutableMemtable.Size())
	for _, entry := range store.ImmutableMemtable.Entries() {
		records = append(records, serializer.Record{Key: entry.Key, Value: entry.Value})
	}

	filePath := sstable.FileName(store.DataDir, store.nextSequence)
	store.nextSequence++
	table := sstable.New(filePath)
	if err := table.Write(records); err != nil {
		return err
	}

	store.SSTables = append([]*sstable.SSTable{table}, store.SSTables...)
	store.ImmutableMemtable = nil
	return nil
}

func reverseTables(tables []*sstable.SSTable) {
	for left, right := 0, len(tables)-1; left < right; left, right = left+1, right-1 {
		tables[left], tables[right] = tables[right], tables[left]
	}
}
