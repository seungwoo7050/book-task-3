package sparseindex

import (
	"strconv"

	"study.local/go/shared/serializer"
)

type Entry struct {
	Key    string
	Offset int64
}

type Range struct {
	Start int64
	End   int64
}

type Index struct {
	BlockSize int
	Entries   []Entry
}

func New(blockSize int) *Index {
	if blockSize <= 0 {
		blockSize = 16
	}
	return &Index{BlockSize: blockSize}
}

func (index *Index) Build(entries []Entry) {
	index.Entries = index.Entries[:0]
	for i, entry := range entries {
		if i%index.BlockSize == 0 {
			index.Entries = append(index.Entries, entry)
		}
	}
}

func (index *Index) FindBlock(key string, dataSize int64) (Range, bool) {
	if len(index.Entries) == 0 {
		return Range{}, false
	}
	if key < index.Entries[0].Key {
		return Range{}, false
	}

	low := 0
	high := len(index.Entries) - 1
	block := 0
	for low <= high {
		mid := (low + high) / 2
		if index.Entries[mid].Key <= key {
			block = mid
			low = mid + 1
		} else {
			high = mid - 1
		}
	}

	start := index.Entries[block].Offset
	end := dataSize
	if block+1 < len(index.Entries) {
		end = index.Entries[block+1].Offset
	}
	return Range{Start: start, End: end}, true
}

func (index *Index) Serialize() ([]byte, error) {
	records := make([]serializer.Record, 0, len(index.Entries))
	for _, entry := range index.Entries {
		offset := strconv.FormatInt(entry.Offset, 10)
		records = append(records, serializer.Record{Key: entry.Key, Value: serializer.StringPtr(offset)})
	}
	return serializer.EncodeAll(records)
}

func Deserialize(buffer []byte, blockSize int) (*Index, error) {
	records, err := serializer.DecodeAll(buffer)
	if err != nil {
		return nil, err
	}
	index := New(blockSize)
	for _, record := range records {
		offset, err := strconv.ParseInt(*record.Value, 10, 64)
		if err != nil {
			return nil, err
		}
		index.Entries = append(index.Entries, Entry{Key: record.Key, Offset: offset})
	}
	return index, nil
}
