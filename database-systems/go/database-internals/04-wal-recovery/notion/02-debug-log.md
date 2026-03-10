# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. 손상된 trailing record를 끝까지 읽는 경우
- 의심 파일: `../internal/wal/wal.go`
- 깨지는 징후: 중간 corruption 이후 garbage를 더 읽어 버리면 복원 상태가 예측 불가능해집니다.
- 확인 테스트: `TestStopAtCorruptedRecord`, `TestRecoverNonexistentAndTruncated`
- 다시 볼 질문: checksum 불일치나 길이 부족이 나오면 그 지점에서 replay를 중단하는가?

### 2. delete replay가 live value 삭제와 tombstone 기록을 혼동하는 경우
- 의심 파일: `../internal/store/store.go`
- 깨지는 징후: 복구 후 삭제된 key가 되살아나거나 missing과 tombstone이 섞이면 WAL type decode가 틀린 것입니다.
- 확인 테스트: `TestRecoverDeleteRecords`
- 다시 볼 질문: record type이 delete일 때 store에 어떤 상태를 남겨야 다음 flush가 올바르게 동작하는가?

### 3. flush 이후에도 오래된 active WAL을 계속 쓰는 경우
- 의심 파일: `../internal/store/store.go`
- 깨지는 징후: WAL rotation이 안 되면 이미 SSTable로 굳힌 기록을 다시 replay하게 됩니다.
- 확인 테스트: `TestStoreRecoversFromWALAfterReopen`, `TestForceFlushRotatesWAL`
- 다시 볼 질문: `active.wal`을 새로 만들거나 truncate하는 시점이 flush 완료와 정확히 맞물리는가?
