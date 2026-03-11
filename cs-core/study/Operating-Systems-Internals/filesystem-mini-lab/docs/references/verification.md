# Filesystem Mini Lab 검증 기록

## canonical 명령

```bash
cd problem
make test
make run-demo
```

## 테스트가 고정하는 것

- create/write/read round trip
- unlink 이후 inode/block free list 정리
- reopen persistence
- `after_prepare` crash discard
- `after_commit` crash replay

## demo에서 확인할 것

- write 후 파일 목록과 사용 중 inode/block 수가 출력된다
- crash 후 `recover` 결과가 `replayed / discarded` 형태로 나온다
- recovery 뒤 `journal_entries=0` 상태로 돌아간다
