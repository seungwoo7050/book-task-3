package bloomfilter

import (
	"encoding/binary"
	"errors"
	"math"

	"study.local/go/shared/hash"
)

type Filter struct {
	BitCount      uint32
	HashFunctions uint32
	bits          []byte
}

func New(expectedItems int, falsePositiveRate float64) *Filter {
	if expectedItems <= 0 {
		expectedItems = 1
	}
	if falsePositiveRate <= 0 || falsePositiveRate >= 1 {
		falsePositiveRate = 0.01
	}

	m := math.Ceil(-(float64(expectedItems) * math.Log(falsePositiveRate)) / (math.Ln2 * math.Ln2))
	k := math.Round((m / float64(expectedItems)) * math.Ln2)
	if k < 1 {
		k = 1
	}

	return &Filter{
		BitCount:      uint32(m),
		HashFunctions: uint32(k),
		bits:          make([]byte, int(math.Ceil(m/8))),
	}
}

func (filter *Filter) Add(key string) {
	for _, position := range filter.positions(key) {
		filter.setBit(position)
	}
}

func (filter *Filter) MightContain(key string) bool {
	for _, position := range filter.positions(key) {
		if !filter.getBit(position) {
			return false
		}
	}
	return true
}

func (filter *Filter) Serialize() []byte {
	buffer := make([]byte, 8+len(filter.bits))
	binary.BigEndian.PutUint32(buffer[0:4], filter.BitCount)
	binary.BigEndian.PutUint32(buffer[4:8], filter.HashFunctions)
	copy(buffer[8:], filter.bits)
	return buffer
}

func Deserialize(buffer []byte) (*Filter, error) {
	if len(buffer) < 8 {
		return nil, errors.New("bloomfilter: buffer too small")
	}
	filter := &Filter{
		BitCount:      binary.BigEndian.Uint32(buffer[0:4]),
		HashFunctions: binary.BigEndian.Uint32(buffer[4:8]),
		bits:          append([]byte(nil), buffer[8:]...),
	}
	if filter.BitCount == 0 || filter.HashFunctions == 0 {
		return nil, errors.New("bloomfilter: malformed header")
	}
	return filter, nil
}

func (filter *Filter) positions(key string) []uint32 {
	h1 := hash.MurmurHash3([]byte(key), 0)
	h2 := hash.MurmurHash3([]byte(key), 42)
	positions := make([]uint32, 0, filter.HashFunctions)
	for i := uint32(0); i < filter.HashFunctions; i++ {
		positions = append(positions, (h1+i*h2)%filter.BitCount)
	}
	return positions
}

func (filter *Filter) setBit(position uint32) {
	byteIndex := position / 8
	bitIndex := position % 8
	filter.bits[byteIndex] |= 1 << bitIndex
}

func (filter *Filter) getBit(position uint32) bool {
	byteIndex := position / 8
	bitIndex := position % 8
	return filter.bits[byteIndex]&(1<<bitIndex) != 0
}
