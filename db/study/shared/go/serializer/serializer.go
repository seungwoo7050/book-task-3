package serializer

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"math"
)

const TombstoneMarker = math.MaxUint32

// Record is a binary-serializable key-value pair. Nil Value means tombstone.
type Record struct {
	Key   string
	Value *string
}

// StringPtr helps tests and demos construct live records.
func StringPtr(value string) *string {
	copyValue := value
	return &copyValue
}

// EncodeRecord serializes a record into [key_len][val_len][key][value].
func EncodeRecord(record Record) ([]byte, error) {
	keyBytes := []byte(record.Key)
	valueBytes := []byte{}
	valueLength := uint32(TombstoneMarker)
	if record.Value != nil {
		valueBytes = []byte(*record.Value)
		valueLength = uint32(len(valueBytes))
	}

	buffer := bytes.NewBuffer(make([]byte, 0, 8+len(keyBytes)+len(valueBytes)))
	if err := binary.Write(buffer, binary.BigEndian, uint32(len(keyBytes))); err != nil {
		return nil, err
	}
	if err := binary.Write(buffer, binary.BigEndian, valueLength); err != nil {
		return nil, err
	}
	if _, err := buffer.Write(keyBytes); err != nil {
		return nil, err
	}
	if _, err := buffer.Write(valueBytes); err != nil {
		return nil, err
	}

	return buffer.Bytes(), nil
}

// EncodeAll serializes multiple records into a single buffer.
func EncodeAll(records []Record) ([]byte, error) {
	buffers := make([][]byte, 0, len(records))
	totalLength := 0
	for _, record := range records {
		encoded, err := EncodeRecord(record)
		if err != nil {
			return nil, err
		}
		buffers = append(buffers, encoded)
		totalLength += len(encoded)
	}

	result := make([]byte, 0, totalLength)
	for _, encoded := range buffers {
		result = append(result, encoded...)
	}
	return result, nil
}

// DecodeRecord decodes one record starting at offset and reports bytes consumed.
func DecodeRecord(data []byte, offset int) (Record, int, error) {
	if len(data) < offset+8 {
		return Record{}, 0, errors.New("serializer: not enough bytes for header")
	}

	keyLength := binary.BigEndian.Uint32(data[offset : offset+4])
	valueLength := binary.BigEndian.Uint32(data[offset+4 : offset+8])

	actualValueLength := valueLength
	if valueLength == TombstoneMarker {
		actualValueLength = 0
	}

	totalLength := 8 + int(keyLength) + int(actualValueLength)
	if len(data) < offset+totalLength {
		return Record{}, 0, fmt.Errorf("serializer: truncated record at offset %d", offset)
	}

	keyStart := offset + 8
	keyEnd := keyStart + int(keyLength)
	valueStart := keyEnd
	valueEnd := valueStart + int(actualValueLength)

	record := Record{Key: string(data[keyStart:keyEnd])}
	if valueLength != TombstoneMarker {
		record.Value = StringPtr(string(data[valueStart:valueEnd]))
	}

	return record, totalLength, nil
}

// DecodeAll decodes every record from a contiguous byte slice.
func DecodeAll(data []byte) ([]Record, error) {
	records := []Record{}
	offset := 0
	for offset < len(data) {
		record, bytesRead, err := DecodeRecord(data, offset)
		if err != nil {
			return nil, err
		}
		records = append(records, record)
		offset += bytesRead
	}
	return records, nil
}
