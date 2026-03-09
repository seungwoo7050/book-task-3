package sstable

import (
	"encoding/binary"
	"errors"
	"fmt"
	"path/filepath"
	"strconv"

	"study.local/shared/fileio"
	"study.local/shared/serializer"
)

type IndexEntry struct {
	Key    string
	Offset int64
}

type SSTable struct {
	FilePath string
	Index    []IndexEntry
}

func New(filePath string) *SSTable {
	return &SSTable{FilePath: filePath}
}

func (table *SSTable) Write(records []serializer.Record) error {
	indexEntries := make([]IndexEntry, 0, len(records))
	dataSection := make([]byte, 0)
	var offset int64
	for _, record := range records {
		encoded, err := serializer.EncodeRecord(record)
		if err != nil {
			return err
		}
		indexEntries = append(indexEntries, IndexEntry{Key: record.Key, Offset: offset})
		dataSection = append(dataSection, encoded...)
		offset += int64(len(encoded))
	}

	indexRecords := make([]serializer.Record, 0, len(indexEntries))
	for _, entry := range indexEntries {
		indexRecords = append(indexRecords, serializer.Record{
			Key:   entry.Key,
			Value: serializer.StringPtr(strconv.FormatInt(entry.Offset, 10)),
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
		return errors.New("sstable: file too small")
	}

	footer, err := handle.ReadAt(fileSize-8, 8)
	if err != nil {
		return err
	}
	dataSectionSize := int64(binary.BigEndian.Uint32(footer[0:4]))
	indexSectionSize := int64(binary.BigEndian.Uint32(footer[4:8]))
	if dataSectionSize+indexSectionSize+8 != fileSize {
		return fmt.Errorf("sstable: malformed footer")
	}

	indexBuffer, err := handle.ReadAt(dataSectionSize, int(indexSectionSize))
	if err != nil {
		return err
	}
	indexRecords, err := serializer.DecodeAll(indexBuffer)
	if err != nil {
		return err
	}
	table.Index = make([]IndexEntry, 0, len(indexRecords))
	for _, record := range indexRecords {
		offset, err := strconv.ParseInt(*record.Value, 10, 64)
		if err != nil {
			return err
		}
		table.Index = append(table.Index, IndexEntry{Key: record.Key, Offset: offset})
	}
	return nil
}

func (table *SSTable) Lookup(key string) (*string, bool, error) {
	index := table.binarySearch(key)
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
	recordBuffer, err := handle.ReadAt(table.Index[index].Offset, 8+int(keyLength)+int(actualValueLength))
	if err != nil {
		return nil, false, err
	}
	record, _, err := serializer.DecodeRecord(recordBuffer, 0)
	if err != nil {
		return nil, false, err
	}
	return record.Value, true, nil
}

func FileName(dataDir string, sequence int) string {
	return filepath.Join(dataDir, fmt.Sprintf("%06d.sst", sequence))
}

func (table *SSTable) binarySearch(key string) int {
	low := 0
	high := len(table.Index) - 1
	for low <= high {
		mid := (low + high) / 2
		switch {
		case table.Index[mid].Key == key:
			return mid
		case table.Index[mid].Key < key:
			low = mid + 1
		default:
			high = mid - 1
		}
	}
	return -1
}
