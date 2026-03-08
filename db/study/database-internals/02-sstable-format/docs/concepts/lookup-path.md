# Lookup Path

- reopen 시점에는 footer를 읽어 index section 위치를 계산한다.
- index를 메모리에 적재한 뒤 key에 대해 binary search를 수행한다.
- 찾은 offset에서 record header만 먼저 읽고 전체 길이를 계산한 뒤 본 record를 다시 읽는다.
- malformed footer나 truncated record는 조용히 무시하지 않고 에러로 다뤄야 한다.

