# Recovery Policy

- header가 13바이트보다 짧으면 truncated header로 보고 중단한다.
- payload 길이가 부족하면 truncated payload로 보고 중단한다.
- CRC mismatch가 나면 corruption으로 보고 중단한다.
- 이 프로젝트는 "손상 지점 이후는 신뢰하지 않는다"는 보수적 정책을 채택한다.

