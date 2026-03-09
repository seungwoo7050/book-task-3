package store

import (
	"path/filepath"
	"strconv"
	"strings"

	"study.local/database-internals/04-wal-recovery/internal/skiplist"
	"study.local/database-internals/04-wal-recovery/internal/sstable"
	"study.local/database-internals/04-wal-recovery/internal/wal"
	"study.local/shared/fileio"
	"study.local/shared/serializer"
)

const DefaultMemtableThreshold = 64 * 1024

type DurableStore struct {
	DataDir               string
	WALPath               string
	Memtable              *skiplist.SkipList
	SSTables              []*sstable.SSTable
	MemtableSizeThreshold int
	nextSequence          int
	writeAheadLog         *wal.WriteAheadLog
}

func New(dataDir string, memtableSizeThreshold int, fsyncEnabled bool) *DurableStore {
	if memtableSizeThreshold == 0 {
		memtableSizeThreshold = DefaultMemtableThreshold
	}
	walPath := filepath.Join(dataDir, "active.wal")
	return &DurableStore{
		DataDir:               dataDir,
		WALPath:               walPath,
		Memtable:              skiplist.New(),
		MemtableSizeThreshold: memtableSizeThreshold,
		nextSequence:          1,
		writeAheadLog:         wal.New(walPath, fsyncEnabled),
	}
}

func (store *DurableStore) Open() error {
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
		sequence, err := strconv.Atoi(strings.TrimSuffix(fileName, ".sst"))
		if err == nil && sequence >= store.nextSequence {
			store.nextSequence = sequence + 1
		}
	}
	reverseTables(store.SSTables)

	records, err := wal.New(store.WALPath, false).Recover()
	if err != nil {
		return err
	}
	for _, record := range records {
		if record.Type == "delete" {
			store.Memtable.Delete(record.Key)
			continue
		}
		store.Memtable.Put(record.Key, *record.Value)
	}

	return store.writeAheadLog.Open()
}

func (store *DurableStore) Put(key, value string) error {
	if err := store.writeAheadLog.AppendPut(key, value); err != nil {
		return err
	}
	store.Memtable.Put(key, value)
	return store.maybeFlush()
}

func (store *DurableStore) Delete(key string) error {
	if err := store.writeAheadLog.AppendDelete(key); err != nil {
		return err
	}
	store.Memtable.Delete(key)
	return store.maybeFlush()
}

func (store *DurableStore) Get(key string) (*string, bool, error) {
	if value, state := store.Memtable.Get(key); state != skiplist.Missing {
		return value, true, nil
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

func (store *DurableStore) ForceFlush() error {
	if store.Memtable.Size() == 0 {
		return nil
	}
	records := make([]serializer.Record, 0, store.Memtable.Size())
	for _, entry := range store.Memtable.Entries() {
		records = append(records, serializer.Record{Key: entry.Key, Value: entry.Value})
	}

	filePath := sstable.FileName(store.DataDir, store.nextSequence)
	store.nextSequence++
	table := sstable.New(filePath)
	if err := table.Write(records); err != nil {
		return err
	}
	store.SSTables = append([]*sstable.SSTable{table}, store.SSTables...)

	if err := store.writeAheadLog.Close(); err != nil {
		return err
	}
	if err := fileio.RemoveFile(store.WALPath); err != nil {
		return err
	}
	store.Memtable.Clear()
	store.writeAheadLog = wal.New(store.WALPath, store.writeAheadLog.FsyncEnabled)
	return store.writeAheadLog.Open()
}

func (store *DurableStore) Close() error {
	return store.writeAheadLog.Close()
}

func (store *DurableStore) maybeFlush() error {
	if store.Memtable.ByteSize() < store.MemtableSizeThreshold {
		return nil
	}
	return store.ForceFlush()
}

func reverseTables(tables []*sstable.SSTable) {
	for left, right := 0, len(tables)-1; left < right; left, right = left+1, right-1 {
		tables[left], tables[right] = tables[right], tables[left]
	}
}
