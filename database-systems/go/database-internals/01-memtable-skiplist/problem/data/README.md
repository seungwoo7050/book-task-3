# Data Notes

이 프로젝트는 외부 fixture가 핵심은 아닙니다. 학습 포인트는 데이터 파일이 아니라 `tests/skiplist_test.go`가 어떤 상태 전이를 검증하는지 읽는 데 있습니다.

- 먼저 테스트를 읽고 어떤 입력 조합이 중요한지 파악합니다.
- 추가 fixture가 필요해지면 tombstone과 ordered iteration이 동시에 드러나는 사례를 우선 만들어 보세요.
