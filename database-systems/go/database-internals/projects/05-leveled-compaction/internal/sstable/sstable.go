package sstable

import (
	"encoding/binary"
	"errors"
	"fmt"
	"path/filepath"
	"strconv"

	"study.local/go/shared/fileio"
	"study.local/go/shared/serializer"
)

type IndexEntry struct {
	Key    string
	Offset int64
}

type SSTable struct {
	FilePath        string
	Index           []IndexEntry
	dataSectionSize int64
}

func New(filePath string) *SSTable {
	return &SSTable{FilePath: filePath}
}

func (table *SSTable) Write(records []serializer.Record) error {
	if err := validateSorted(records); err != nil {
		return err
	}

	dataSection := make([]byte, 0)
	indexEntries := make([]IndexEntry, 0, len(records))
	var offset int64

	for _, record := range records {
		encoded, err := serializer.EncodeRecord(record)
		if err != nil {
			return err
		}
		dataSection = append(dataSection, encoded...)
		indexEntries = append(indexEntries, IndexEntry{Key: record.Key, Offset: offset})
		offset += int64(len(encoded))
	}

	indexRecords := make([]serializer.Record, 0, len(indexEntries))
	for _, entry := range indexEntries {
		offsetString := strconv.FormatInt(entry.Offset, 10)
		indexRecords = append(indexRecords, serializer.Record{
			Key:   entry.Key,
			Value: serializer.StringPtr(offsetString),
		})
	}

	indexSection, err := serializer.EncodeAll(indexRecords)
	if err != nil {
		return err
	}

	footer := make([]byte, 8)
	binary.BigEndian.PutUint32(footer[0:4], uint32(len(dataSection)))
	binary.BigEndian.PutUint32(footer[4:8], uint32(len(indexSection)))

	handle := fileio.NewHandle(table.FilePath)
	if err := handle.Open("w"); err != nil {
		return err
	}
	defer handle.Close()

	if _, err := handle.Append(dataSection); err != nil {
		return err
	}
	if _, err := handle.Append(indexSection); err != nil {
		return err
	}
	if _, err := handle.Append(footer); err != nil {
		return err
	}
	if err := handle.Sync(); err != nil {
		return err
	}

	table.Index = indexEntries
	table.dataSectionSize = int64(len(dataSection))
	return nil
}

func (table *SSTable) LoadIndex() error {
	handle := fileio.NewHandle(table.FilePath)
	if err := handle.Open("r"); err != nil {
		return err
	}
	defer handle.Close()

	fileSize, err := handle.Size()
	if err != nil {
		return err
	}
	if fileSize < 8 {
		return errors.New("sstable: file too small for footer")
	}

	footer, err := handle.ReadAt(fileSize-8, 8)
	if err != nil {
		return err
	}
	dataSectionSize := int64(binary.BigEndian.Uint32(footer[0:4]))
	indexSectionSize := int64(binary.BigEndian.Uint32(footer[4:8]))
	if dataSectionSize+indexSectionSize+8 != fileSize {
		return fmt.Errorf("sstable: malformed footer for %s", table.FilePath)
	}

	indexBytes, err := handle.ReadAt(dataSectionSize, int(indexSectionSize))
	if err != nil {
		return err
	}
	indexRecords, err := serializer.DecodeAll(indexBytes)
	if err != nil {
		return err
	}

	table.Index = make([]IndexEntry, 0, len(indexRecords))
	for _, record := range indexRecords {
		if record.Value == nil {
			return errors.New("sstable: index record cannot be tombstone")
		}
		offset, err := strconv.ParseInt(*record.Value, 10, 64)
		if err != nil {
			return err
		}
		table.Index = append(table.Index, IndexEntry{Key: record.Key, Offset: offset})
	}
	table.dataSectionSize = dataSectionSize
	return nil
}

func (table *SSTable) Get(key string) (*string, bool, error) {
	if len(table.Index) == 0 {
		if err := table.LoadIndex(); err != nil {
			return nil, false, err
		}
	}

	index := binarySearch(table.Index, key)
	if index == -1 {
		return nil, false, nil
	}

	handle := fileio.NewHandle(table.FilePath)
	if err := handle.Open("r"); err != nil {
		return nil, false, err
	}
	defer handle.Close()

	header, err := handle.ReadAt(table.Index[index].Offset, 8)
	if err != nil {
		return nil, false, err
	}
	keyLength := binary.BigEndian.Uint32(header[0:4])
	valueLength := binary.BigEndian.Uint32(header[4:8])
	actualValueLength := valueLength
	if valueLength == serializer.TombstoneMarker {
		actualValueLength = 0
	}

	recordBuffer, err := handle.ReadAt(table.Index[index].Offset, int(8+keyLength+actualValueLength))
	if err != nil {
		return nil, false, err
	}
	record, _, err := serializer.DecodeRecord(recordBuffer, 0)
	if err != nil {
		return nil, false, err
	}
	return record.Value, true, nil
}

func (table *SSTable) ReadAll() ([]serializer.Record, error) {
	handle := fileio.NewHandle(table.FilePath)
	if err := handle.Open("r"); err != nil {
		return nil, err
	}
	defer handle.Close()

	fileSize, err := handle.Size()
	if err != nil {
		return nil, err
	}
	if fileSize < 8 {
		return nil, errors.New("sstable: file too small for footer")
	}

	footer, err := handle.ReadAt(fileSize-8, 8)
	if err != nil {
		return nil, err
	}
	dataSectionSize := int64(binary.BigEndian.Uint32(footer[0:4]))
	indexSectionSize := int64(binary.BigEndian.Uint32(footer[4:8]))
	if dataSectionSize+indexSectionSize+8 != fileSize {
		return nil, errors.New("sstable: malformed footer")
	}

	dataBytes, err := handle.ReadAt(0, int(dataSectionSize))
	if err != nil {
		return nil, err
	}
	return serializer.DecodeAll(dataBytes)
}

func FileName(dataDir string, sequence int) string {
	return filepath.Join(dataDir, fmt.Sprintf("%06d.sst", sequence))
}

func validateSorted(records []serializer.Record) error {
	for i := 1; i < len(records); i++ {
		if records[i-1].Key > records[i].Key {
			return fmt.Errorf("sstable: records must be sorted, %q > %q", records[i-1].Key, records[i].Key)
		}
	}
	return nil
}

func binarySearch(index []IndexEntry, key string) int {
	low := 0
	high := len(index) - 1
	for low <= high {
		mid := (low + high) / 2
		switch {
		case index[mid].Key == key:
			return mid
		case index[mid].Key < key:
			low = mid + 1
		default:
			high = mid - 1
		}
	}
	return -1
}
