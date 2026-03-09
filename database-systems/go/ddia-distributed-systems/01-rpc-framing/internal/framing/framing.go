package framing

import (
	"encoding/binary"
	"encoding/json"
	"errors"
)

func Encode(message any) ([]byte, error) {
	payload, err := json.Marshal(message)
	if err != nil {
		return nil, err
	}
	frame := make([]byte, 4+len(payload))
	binary.BigEndian.PutUint32(frame[0:4], uint32(len(payload)))
	copy(frame[4:], payload)
	return frame, nil
}

type Decoder struct {
	buffer []byte
}

func (decoder *Decoder) Feed(chunk []byte) ([][]byte, error) {
	decoder.buffer = append(decoder.buffer, chunk...)
	messages := make([][]byte, 0)

	for len(decoder.buffer) >= 4 {
		payloadLength := binary.BigEndian.Uint32(decoder.buffer[0:4])
		totalLength := int(4 + payloadLength)
		if totalLength < 4 {
			return nil, errors.New("framing: invalid frame length")
		}
		if len(decoder.buffer) < totalLength {
			break
		}
		payload := append([]byte(nil), decoder.buffer[4:totalLength]...)
		messages = append(messages, payload)
		decoder.buffer = append([]byte(nil), decoder.buffer[totalLength:]...)
	}

	return messages, nil
}
