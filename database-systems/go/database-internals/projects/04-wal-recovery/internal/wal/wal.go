package wal

import (
	"encoding/binary"
	"errors"
	"os"

	"study.local/go/shared/fileio"
	"study.local/go/shared/hash"
	"study.local/go/shared/serializer"
)

const (
	OpPut    byte = 0x01
	OpDelete byte = 0x02
)

type Record struct {
	Type  string
	Key   string
	Value *string
}

type WriteAheadLog struct {
	FilePath     string
	FsyncEnabled bool
	handle       *fileio.FileHandle
}

func New(filePath string, fsyncEnabled bool) *WriteAheadLog {
	return &WriteAheadLog{
		FilePath:     filePath,
		FsyncEnabled: fsyncEnabled,
	}
}

func (log *WriteAheadLog) Open() error {
	log.handle = fileio.NewHandle(log.FilePath)
	return log.handle.Open("a")
}

func (log *WriteAheadLog) AppendPut(key, value string) error {
	copyValue := value
	return log.appendRecord(OpPut, key, &copyValue)
}

func (log *WriteAheadLog) AppendDelete(key string) error {
	return log.appendRecord(OpDelete, key, nil)
}

func (log *WriteAheadLog) Recover() ([]Record, error) {
	handle := fileio.NewHandle(log.FilePath)
	if err := handle.Open("r"); err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return []Record{}, nil
		}
		return nil, err
	}
	defer handle.Close()

	buffer, err := handle.ReadAll()
	if err != nil {
		return nil, err
	}

	records := []Record{}
	offset := 0
	for offset < len(buffer) {
		if offset+13 > len(buffer) {
			break
		}

		storedCRC := binary.BigEndian.Uint32(buffer[offset : offset+4])
		recordType := buffer[offset+4]
		keyLength := binary.BigEndian.Uint32(buffer[offset+5 : offset+9])
		valueLength := binary.BigEndian.Uint32(buffer[offset+9 : offset+13])
		actualValueLength := valueLength
		if valueLength == serializer.TombstoneMarker {
			actualValueLength = 0
		}
		recordSize := 13 + int(keyLength) + int(actualValueLength)
		if offset+recordSize > len(buffer) {
			break
		}

		payload := buffer[offset+4 : offset+recordSize]
		if hash.CRC32(payload) != storedCRC {
			break
		}

		keyStart := offset + 13
		keyEnd := keyStart + int(keyLength)
		record := Record{
			Key: string(buffer[keyStart:keyEnd]),
		}
		if recordType == OpDelete {
			record.Type = "delete"
		} else {
			record.Type = "put"
			valueStart := keyEnd
			valueEnd := valueStart + int(actualValueLength)
			record.Value = serializer.StringPtr(string(buffer[valueStart:valueEnd]))
		}

		records = append(records, record)
		offset += recordSize
	}

	return records, nil
}

func (log *WriteAheadLog) Close() error {
	if log.handle == nil {
		return nil
	}
	err := log.handle.Close()
	log.handle = nil
	return err
}

func (log *WriteAheadLog) appendRecord(recordType byte, key string, value *string) error {
	if log.handle == nil {
		return errors.New("wal: append on closed log")
	}

	keyBytes := []byte(key)
	valueBytes := []byte{}
	valueLength := uint32(serializer.TombstoneMarker)
	if value != nil {
		valueBytes = []byte(*value)
		valueLength = uint32(len(valueBytes))
	}

	header := make([]byte, 9)
	header[0] = recordType
	binary.BigEndian.PutUint32(header[1:5], uint32(len(keyBytes)))
	binary.BigEndian.PutUint32(header[5:9], valueLength)

	payload := append(header, keyBytes...)
	payload = append(payload, valueBytes...)

	record := make([]byte, 4)
	binary.BigEndian.PutUint32(record[0:4], hash.CRC32(payload))
	record = append(record, payload...)

	if _, err := log.handle.Append(record); err != nil {
		return err
	}
	if log.FsyncEnabled {
		return log.handle.Sync()
	}
	return nil
}
