# 10 범위를 다시 좁히기: WAL은 로그 추가가 아니라 write path 재정의다

처음엔 이 프로젝트를 "앞 프로젝트에 로그 파일 하나 추가하는 단계" 정도로 생각하기 쉬웠다. 그런데 문제 정의와 테스트를 다시 읽어 보니 실제로 바뀌는 건 훨씬 크다. write의 인정 시점, 손상 처리 정책, flush 이후 파일 수명까지 모두 다시 정의된다.

## Phase 1. 테스트 이름이 이미 durable write path를 공개 계약으로 만든다

`tests/test_wal_recovery.py`를 다시 훑어 보면 범위가 금방 드러난다. `test_recover_put_records`, `test_recover_delete_records`, `test_recover_many_records`는 WAL record format과 replay를 보여 주고, `test_stop_at_corrupted_record`, `test_recover_nonexistent_and_truncated`는 failure policy를 공개 계약으로 끌어올린다. 마지막으로 `test_store_recovers_from_wal_after_reopen`, `test_force_flush_rotates_wal`은 이제 WAL이 store lifecycle 전체와 연결됐다는 사실을 못 박는다.

즉 이 슬롯은 "WAL parser"에서 멈추지 않는다. reopen 시 memtable을 어떻게 다시 만들고, flush가 끝난 뒤 active WAL을 어떻게 잘라내는지까지 포함한다.

이번 재실행:

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/02-wal-recovery
PYTHONPATH=src python3 -m pytest
```

결과:

```text
7 passed, 1 warning in 0.04s
```

여기서 경고는 `pytest_asyncio` deprecation이라 durability semantics와는 무관했다.

## Phase 2. 문제 정의가 "보수적 recovery"를 의도적으로 선택한다

`problem/README.md`와 `docs/concepts/recovery-policy.md`를 같이 보면 이 프로젝트의 톤이 더 분명해진다. 핵심은 가능한 많은 레코드를 살리는 게 아니라, 첫 손상 지점 이후를 신뢰하지 않는 것이다.

- header가 짧으면 중단
- payload 길이가 부족하면 중단
- CRC mismatch면 중단

이건 꽤 중요한 태도다. WAL recovery를 "어떻게든 salvage"가 아니라 "확실한 prefix만 복원"의 문제로 잡는 셈이기 때문이다. 이후 더 복잡한 durability 설계로 갈수록 이 판단은 자주 다시 등장한다.

## Phase 3. 파일 구조도 write path가 바뀌었음을 보여 준다

소스 파일을 다시 보면 `store.py` 안에 `WriteAheadLog`, `SSTable`, `DurableStore`가 같이 들어 있다. 바로 앞 슬롯의 `MiniLSMStore`가 flush/read ordering을 보여 줬다면, 이번엔 같은 저장 엔진 표면에 WAL이 앞단에 끼어들어 순서를 바꾸는 구조다.

즉 질문이 바뀐다.

- 예전: memtable이 언제 flush되는가?
- 지금: memtable에 들어가기 전에 어떤 bytes가 WAL에 먼저 남는가?

이 범위 재설정이 이 슬롯의 진짜 시작점이다.
