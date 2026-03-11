# Journaling Recovery

## metadata-only journaling을 왜 고르는가

toy filesystem에서 journaling을 설명하려면 가장 먼저 “무엇을 보호할 것인가”를 줄여야 한다. 이 프로젝트는 metadata-only journaling만 남겨, inode/root mapping/block bitmap 갱신을 crash-safe하게 만드는 흐름에 집중한다.

- data block은 먼저 기록한다.
- journal은 metadata update intent와 commit 여부를 기록한다.
- crash 뒤 recovery는 committed entry만 replay한다.

## 이 프로젝트에서 일부러 생략한 것

- data journaling
- checksumming
- ordered/writeback mode 비교

그래도 prepared와 committed를 구분하는 것만으로 crash 직전/직후 상태를 충분히 설명할 수 있다.
