# Problem Guide

## 문제 핵심

- 디스크 이미지는 JSON 파일 하나로 고정한다.
- root directory 하나만 지원하고, 파일 연산은 `create`, `write`, `cat`, `ls`, `unlink`, `recover`만 다룬다.
- inode bitmap과 block bitmap이 실제 allocation/free를 반영해야 한다.
- journaling은 metadata-only write-ahead log로 제한하고, crash 이후 `recover`가 committed entry를 replay하고 prepared entry를 폐기해야 한다.

## 이번 범위에서 일부러 뺀 것

- nested directory
- permission bit
- rename
- concurrent access
- data journaling과 checksumming

## canonical 검증

```bash
make test
make run-demo
```

## 성공 기준

- create/write/read/delete가 JSON image 위에서 일관되게 동작한다.
- reopen 후 상태가 유지된다.
- committed journal replay와 incomplete journal discard가 tests로 재현된다.
