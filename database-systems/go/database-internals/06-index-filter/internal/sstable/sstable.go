package sstable

import (
	"encoding/binary"
	"errors"
	"fmt"

	"study.local/database-internals/06-index-filter/internal/bloomfilter"
	"study.local/database-internals/06-index-filter/internal/sparseindex"
	"study.local/shared/fileio"
	"study.local/shared/serializer"
)

var footerMagic = [4]byte{'S', 'I', 'F', '1'}

type LookupStats struct {
	BloomRejected bool
	BytesRead     int64
	BlockRange    sparseindex.Range
}

type Table struct {
	FilePath    string
	BlockSize   int
	DataSize    int64
	BloomOffset int64
	BloomSize   int64
	IndexOffset int64
	IndexSize   int64
	Filter      *bloomfilter.Filter
	Index       *sparseindex.Index
}

func New(filePath string, blockSize int) *Table {
	if blockSize <= 0 {
		blockSize = 16
	}
	return &Table{FilePath: filePath, BlockSize: blockSize}
}

func (table *Table) Write(records []serializer.Record) error {
	if err := validateSorted(records); err != nil {
		return err
	}

	dataSection := make([]byte, 0)
	offsets := make([]sparseindex.Entry, 0, len(records))
	filter := bloomfilter.New(len(records)+1, 0.01)
	var offset int64

	for _, record := range records {
		filter.Add(record.Key)
		encoded, err := serializer.EncodeRecord(record)
		if err != nil {
			return err
		}
		offsets = append(offsets, sparseindex.Entry{Key: record.Key, Offset: offset})
		dataSection = append(dataSection, encoded...)
		offset += int64(len(encoded))
	}

	index := sparseindex.New(table.BlockSize)
	index.Build(offsets)
	indexBytes, err := index.Serialize()
	if err != nil {
		return err
	}
	filterBytes := filter.Serialize()

	table.DataSize = int64(len(dataSection))
	table.BloomOffset = table.DataSize
	table.BloomSize = int64(len(filterBytes))
	table.IndexOffset = table.BloomOffset + table.BloomSize
	table.IndexSize = int64(len(indexBytes))
	table.Filter = filter
	table.Index = index

	footer := make([]byte, 40)
	copy(footer[0:4], footerMagic[:])
	binary.BigEndian.PutUint64(footer[4:12], uint64(table.BloomOffset))
	binary.BigEndian.PutUint64(footer[12:20], uint64(table.BloomSize))
	binary.BigEndian.PutUint64(footer[20:28], uint64(table.IndexOffset))
	binary.BigEndian.PutUint64(footer[28:36], uint64(table.IndexSize))
	binary.BigEndian.PutUint32(footer[36:40], uint32(table.BlockSize))

	handle := fileio.NewHandle(table.FilePath)
	if err := handle.Open("w"); err != nil {
		return err
	}
	defer handle.Close()

	if _, err := handle.Append(dataSection); err != nil {
		return err
	}
	if _, err := handle.Append(filterBytes); err != nil {
		return err
	}
	if _, err := handle.Append(indexBytes); err != nil {
		return err
	}
	if _, err := handle.Append(footer); err != nil {
		return err
	}
	return handle.Sync()
}

func (table *Table) Load() error {
	handle := fileio.NewHandle(table.FilePath)
	if err := handle.Open("r"); err != nil {
		return err
	}
	defer handle.Close()

	fileSize, err := handle.Size()
	if err != nil {
		return err
	}
	if fileSize < 40 {
		return errors.New("sstable: file too small")
	}

	footer, err := handle.ReadAt(fileSize-40, 40)
	if err != nil {
		return err
	}
	if string(footer[0:4]) != string(footerMagic[:]) {
		return errors.New("sstable: invalid footer magic")
	}

	table.BloomOffset = int64(binary.BigEndian.Uint64(footer[4:12]))
	table.BloomSize = int64(binary.BigEndian.Uint64(footer[12:20]))
	table.IndexOffset = int64(binary.BigEndian.Uint64(footer[20:28]))
	table.IndexSize = int64(binary.BigEndian.Uint64(footer[28:36]))
	table.BlockSize = int(binary.BigEndian.Uint32(footer[36:40]))
	table.DataSize = table.BloomOffset

	filterBytes, err := handle.ReadAt(table.BloomOffset, int(table.BloomSize))
	if err != nil {
		return err
	}
	table.Filter, err = bloomfilter.Deserialize(filterBytes)
	if err != nil {
		return err
	}

	indexBytes, err := handle.ReadAt(table.IndexOffset, int(table.IndexSize))
	if err != nil {
		return err
	}
	table.Index, err = sparseindex.Deserialize(indexBytes, table.BlockSize)
	return err
}

func (table *Table) Get(key string) (*string, bool, error) {
	value, ok, _, err := table.GetWithStats(key)
	return value, ok, err
}

func (table *Table) GetWithStats(key string) (*string, bool, LookupStats, error) {
	if table.Filter == nil || table.Index == nil {
		if err := table.Load(); err != nil {
			return nil, false, LookupStats{}, err
		}
	}

	if !table.Filter.MightContain(key) {
		return nil, false, LookupStats{BloomRejected: true}, nil
	}

	block, ok := table.Index.FindBlock(key, table.DataSize)
	if !ok {
		return nil, false, LookupStats{}, nil
	}

	handle := fileio.NewHandle(table.FilePath)
	if err := handle.Open("r"); err != nil {
		return nil, false, LookupStats{}, err
	}
	defer handle.Close()

	buffer, err := handle.ReadAt(block.Start, int(block.End-block.Start))
	if err != nil {
		return nil, false, LookupStats{}, err
	}
	stats := LookupStats{BytesRead: int64(len(buffer)), BlockRange: block}

	offset := 0
	for offset < len(buffer) {
		record, read, err := serializer.DecodeRecord(buffer, offset)
		if err != nil {
			return nil, false, stats, err
		}
		switch {
		case record.Key == key:
			return record.Value, true, stats, nil
		case record.Key > key:
			return nil, false, stats, nil
		}
		offset += read
	}

	return nil, false, stats, nil
}

func validateSorted(records []serializer.Record) error {
	for i := 1; i < len(records); i++ {
		if records[i-1].Key > records[i].Key {
			return fmt.Errorf("sstable: records must be sorted, %q > %q", records[i-1].Key, records[i].Key)
		}
	}
	return nil
}
