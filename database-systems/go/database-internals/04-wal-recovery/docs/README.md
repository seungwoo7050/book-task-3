# Docs Guide

이 디렉터리는 04 WAL Recovery를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/wal-record-format.md`](concepts/wal-record-format.md): WAL 레코드 헤더, checksum, payload 구성이 왜 필요한지 정리합니다.
- [`concepts/recovery-policy.md`](concepts/recovery-policy.md): 손상 이후 stop-on-corruption 정책을 택했을 때의 장단점을 설명합니다.

## 추천 읽기 순서

1. `wal-record-format.md`를 읽으며 핵심 용어를 맞춥니다.
2. `recovery-policy.md`를 읽으며 핵심 용어를 맞춥니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
