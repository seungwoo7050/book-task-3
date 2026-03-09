# WAL Record Format

- record는 `[crc32][type][keyLen][valLen][key][value]` 순서다.
- CRC는 payload 부분만 대상으로 계산한다.
- delete는 `valLen = 0xFFFFFFFF` sentinel로 표현한다.
- 이 형식은 replay 중에 길이와 무결성을 둘 다 점검할 수 있게 해 준다.

