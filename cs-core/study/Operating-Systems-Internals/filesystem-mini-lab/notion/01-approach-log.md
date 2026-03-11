# 01 Approach Log

## 설계 선택

- nested directory를 뺀 대신 root mapping, inode table, block bitmap 관계가 바로 드러나게 했다.
- disk image를 JSON 하나로 두어 test와 demo가 파일 하나만 다루게 했다.
- write는 data block을 먼저 기록하고 journal로 metadata만 보호하는 흐름으로 고정했다.
- transaction state를 `prepared`와 `committed`로만 나눠 recovery 규칙을 단순하게 유지했다.

## crash stage를 노출한 이유

- recovery 테스트를 deterministic하게 만들려면 “언제 crash가 났는가”를 코드 수준에서 고정해야 했다.
- 그래서 `after_prepare`, `after_commit` 시점을 예외로 강제해 journal 상태를 정확히 재현하게 했다.
