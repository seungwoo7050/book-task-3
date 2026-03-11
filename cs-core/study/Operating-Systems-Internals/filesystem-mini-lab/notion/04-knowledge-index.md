# 04 Knowledge Index

## 핵심 용어

- inode table: 파일 메타데이터와 block pointer를 저장하는 표
- block bitmap: 사용 중인 data block을 기록하는 free-list 대체 표면
- metadata journaling: 메타데이터 변경을 commit/replay 가능한 형태로 보호하는 방식
- crash recovery: 중간 상태의 journal을 읽어 committed만 반영하고 incomplete 작업을 버리는 과정

## 같이 보면 좋은 파일

- `../docs/concepts/inode-and-blocks.md`
- `../docs/concepts/journaling-recovery.md`
- `../docs/concepts/transaction-states.md`
- `../python/tests/test_os_mini_fs.py`
