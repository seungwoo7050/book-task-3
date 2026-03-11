# Filesystem Mini Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 root-only toy filesystem을 통해 inode, block bitmap, journal, recovery가 서로 어떻게 연결되는지 설명한다. 커널 파일시스템의 모든 기능을 다루기보다 “최소 모델에서 어떤 메타데이터가 꼭 필요한가”를 먼저 고정하는 것이 목표다.

## 누구를 위한 문서인가

- inode와 data block 관계를 글과 예제로 먼저 이해하고 싶은 학습자
- journaling recovery를 너무 큰 코드베이스 없이 배우고 싶은 사람
- create/write/unlink가 allocation 표면에서 어떤 흔적을 남기는지 보고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/inode-and-blocks.md`](concepts/inode-and-blocks.md)
2. [`concepts/journaling-recovery.md`](concepts/journaling-recovery.md)
3. [`concepts/transaction-states.md`](concepts/transaction-states.md)
4. [`references/verification.md`](references/verification.md)
5. [`references/README.md`](references/README.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    inode-and-blocks.md
    journaling-recovery.md
    transaction-states.md
  references/
    verification.md
    README.md
```

## 검증과 연결되는 파일

- image와 journal 모델은 [`../python/src/os_mini_fs/core.py`](../python/src/os_mini_fs/core.py)에 있다.
- recovery 계약은 [`../python/tests/test_os_mini_fs.py`](../python/tests/test_os_mini_fs.py)에 있다.
- demo 흐름은 [`../problem/script/run_demo.py`](../problem/script/run_demo.py)에서 재현된다.
- 현재 검증 신호는 [`references/verification.md`](references/verification.md)에 정리돼 있다.

## 포트폴리오로 확장하는 힌트

- root-only 제약을 걷어내고 path lookup을 추가하면 directory hierarchy까지 이어질 수 있다.
- metadata-only journal 뒤에 data journal이나 copy-on-write를 비교하면 저장장치 설계 이야기로 넓힐 수 있다.
