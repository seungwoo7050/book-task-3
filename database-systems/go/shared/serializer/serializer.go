package serializer

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"math"
)

const TombstoneMarker = math.MaxUint32

// Record는 binary serialization 가능한 key-value pair다. Nil Value는 tombstone을 뜻한다.
type Record struct {
	Key   string
	Value *string
}

// StringPtr는 test와 demo에서 live record를 만들 때 쓰는 helper다.
func StringPtr(value string) *string {
	copyValue := value
	return &copyValue
}

// EncodeRecord는 record를 [key_len][val_len][key][value] 형식으로 직렬화한다.
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

// EncodeAll은 여러 record를 하나의 buffer로 직렬화한다.
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

// DecodeRecord는 offset부터 record 하나를 복원하고 읽은 byte 수를 함께 반환한다.
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

// DecodeAll은 연속된 byte slice에서 모든 record를 복원한다.
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
