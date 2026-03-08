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
	FilePath         string
	Index            []IndexEntry
	dataSectionSize  int64
	indexSectionSize int64
}

func New(filePath string) *SSTable {
	return &SSTable{FilePath: filePath}
}

func (table *SSTable) Write(records []serializer.Record) error {
	if err := validateSorted(records); err != nil {
		return err
	}

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

	if len(dataSection) > int(^uint32(0)) || len(indexSection) > int(^uint32(0)) {
		return errors.New("sstable: section too large for 8-byte footer")
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
	table.indexSectionSize = int64(len(indexSection))
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
	if len(footer) != 8 {
		return errors.New("sstable: incomplete footer")
	}

	dataSectionSize := int64(binary.BigEndian.Uint32(footer[0:4]))
	indexSectionSize := int64(binary.BigEndian.Uint32(footer[4:8]))
	if dataSectionSize < 0 || indexSectionSize < 0 || dataSectionSize+indexSectionSize+8 != fileSize {
		return fmt.Errorf("sstable: malformed footer sizes data=%d index=%d file=%d", dataSectionSize, indexSectionSize, fileSize)
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
		if record.Value == nil {
			return errors.New("sstable: index offset record cannot be tombstone")
		}
		offset, err := strconv.ParseInt(*record.Value, 10, 64)
		if err != nil {
			return err
		}
		table.Index = append(table.Index, IndexEntry{Key: record.Key, Offset: offset})
	}
	table.dataSectionSize = dataSectionSize
	table.indexSectionSize = indexSectionSize
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
	if len(header) != 8 {
		return nil, false, errors.New("sstable: truncated record header")
	}

	keyLength := binary.BigEndian.Uint32(header[0:4])
	valueLength := binary.BigEndian.Uint32(header[4:8])
	actualValueLength := valueLength
	if valueLength == serializer.TombstoneMarker {
		actualValueLength = 0
	}
	recordSize := 8 + int(keyLength) + int(actualValueLength)

	recordBuffer, err := handle.ReadAt(table.Index[index].Offset, recordSize)
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
		return nil, errors.New("sstable: malformed file layout")
	}

	dataBuffer, err := handle.ReadAt(0, int(dataSectionSize))
	if err != nil {
		return nil, err
	}
	return serializer.DecodeAll(dataBuffer)
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

func validateSorted(records []serializer.Record) error {
	for i := 1; i < len(records); i++ {
		if records[i-1].Key > records[i].Key {
			return fmt.Errorf("sstable: records must be sorted, %q > %q", records[i-1].Key, records[i].Key)
		}
	}
	return nil
}

func FileName(dataDir string, sequence int) string {
	return filepath.Join(dataDir, fmt.Sprintf("%06d.sst", sequence))
}
