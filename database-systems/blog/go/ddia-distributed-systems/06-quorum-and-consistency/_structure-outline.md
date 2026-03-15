# Structure Outline

## Core thesis

이 project의 핵심은 `W + R > N` 공식 자체보다, 그 공식을 결정적 responder selection과 single-version register 위에 올려 stale/latest 차이를 재현하는 데 있다.

## Writing plan

1. problem 문서로 이번 단계의 축소된 범위를 먼저 고정한다.
2. `Policy`, `Cluster`, `order` 필드로 모델의 단순화를 설명한다.
3. `Write`에서 version freeze와 all-available fanout을 설명한다.
4. `Read`에서 deterministic responder selection과 highest-version merge를 설명한다.
5. test/demo/임시 boundary check로 검증과 한계를 마무리한다.

## Must-keep evidence

- `TestReadReturnsLatestWhenQuorumsOverlap`
- `TestStaleReadAppearsWhenQuorumsDoNotOverlap`
- `TestWriteFailureDoesNotAdvanceVersion`
- demo의 safe/stale 두 줄
- `replicated=[replica-1 replica-2 replica-3]`
