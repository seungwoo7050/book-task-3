# Merge Ordering

Compaction에서 같은 key가 여러 source에 동시에 존재하면 최신 source의 값만 살아남아야 한다. 이 프로젝트는 `sources[0]`을 newest로 보고 pairwise merge를 왼쪽에서 오른쪽으로 진행한다.

L0 file list는 보통 flush 순서로 append되기 때문에 그대로 읽으면 oldest-first가 된다. 따라서 compaction 입력을 만들 때는 L0 file list를 reverse 해서 newest-first source 배열로 바꾼다.

Tombstone도 일반 value와 같은 우선순위를 가진다. 최신 tombstone이 있으면 older live value는 보이면 안 된다. 단, 더 깊은 레벨에 같은 key의 더 오래된 버전이 남아 있을 수 있으므로 deepest level이 아닐 때는 tombstone을 유지해야 한다.
