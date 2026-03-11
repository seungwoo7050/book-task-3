# Sparse Index Scan

sparse index는 모든 key를 메모리에 들고 있지 않고, block 경계 key만 유지한다. lookup은 다음 순서로 진행된다.

1. Bloom filter가 false면 즉시 miss
2. sparse index에서 `largest indexed key <= target`을 찾음
3. 그 block 범위만 disk에서 읽어 decode
4. block 내부에서 target을 찾거나 key가 지나가면 종료

block이 커질수록 메모리 사용량은 줄고 scan 범위는 늘어난다. 이 프로젝트는 학습용으로 `blockSize`를 명시적으로 노출한다.
