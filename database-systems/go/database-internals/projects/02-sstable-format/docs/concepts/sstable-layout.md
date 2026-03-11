# SSTable Layout

- data section은 record를 연속 배치한 영역이다.
- index section은 각 key가 data section의 어느 offset에서 시작하는지 기록한다.
- footer는 맨 끝 8바이트에 두 section의 길이를 저장한다.
- tombstone은 value length를 `0xFFFFFFFF`로 기록해 delete를 physical remove 대신 logical marker로 남긴다.

