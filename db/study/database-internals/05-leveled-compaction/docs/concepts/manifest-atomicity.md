# Manifest Atomicity

Compaction은 data file 집합과 metadata를 동시에 바꾸는 작업이다. 새 SSTable만 만들고 manifest를 못 바꾸면 reader가 새 파일을 모른다. 반대로 manifest만 먼저 바꾸고 파일 교체가 실패하면 존재하지 않는 파일을 가리키게 된다.

이 프로젝트는 다음 순서를 사용한다.

1. 새 SSTable을 기록한다.
2. 메모리상의 level map을 새 상태로 교체한다.
3. `MANIFEST`를 atomic write로 저장한다.
4. 이전 입력 파일을 제거한다.

완전한 production 시스템이라면 manifest journaling이나 two-phase metadata가 더 필요하지만, 여기서는 학습 목적상 "새 결과가 먼저 존재하고 manifest는 atomic rename으로 갱신된다"는 최소 보장을 유지한다.
