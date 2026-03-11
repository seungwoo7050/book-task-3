# Python 구현 안내

## 구현 범위

- JSON disk image 관리
- inode/block allocation
- metadata-only journal과 recovery
- CLI subcommand와 demo helper

## 어디서부터 읽으면 좋은가

1. `python/src/os_mini_fs/core.py`: image load/save, journal, allocation 로직이 모두 들어 있다.
2. `python/src/os_mini_fs/cli.py`: `mkfs`, `ls`, `create`, `write`, `cat`, `unlink`, `recover` 인터페이스를 본다.
3. `python/tests/test_os_mini_fs.py`: create/write/delete/persistence/recovery 계약을 확인한다.

## 디렉터리 구조

```text
python/
  README.md
  src/os_mini_fs/
    __main__.py
    cli.py
    core.py
  tests/
    test_os_mini_fs.py
```

## 기준 명령

- 검증: `make -C ../problem test`
- demo: `make -C ../problem run-demo`
- 직접 실행: `PYTHONPATH=src python3 -m os_mini_fs --image /tmp/fs.json mkfs --inodes 8 --blocks 16`

## 구현에서 먼저 볼 포인트

- 이 프로젝트는 data block보다 metadata journal 흐름을 설명하는 데 초점을 둔다.
- write는 새 block을 먼저 할당한 뒤 journal commit 후 metadata를 교체한다.
- recovery는 `prepared` entry는 폐기하고 `committed` entry만 replay한다.
