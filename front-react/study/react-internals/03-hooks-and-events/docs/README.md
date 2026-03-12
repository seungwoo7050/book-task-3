# 공개 문서

상태: `verified`

이 디렉터리는 hook slot, effect cleanup, delegated event를 왜 같은 runtime 문제로 묶었는지 설명한다. 구현을 보기 전에 제약과 설계 의도를 빠르게 파악하는 용도다.

## 문서 목록

- [concepts/hook-slot-model.md](concepts/hook-slot-model.md): hook slot과 hook order invariant
- [concepts/effect-timing-and-cleanup.md](concepts/effect-timing-and-cleanup.md): effect setup/cleanup timing
- [concepts/delegated-event-flow.md](concepts/delegated-event-flow.md): delegated event가 runtime tree를 타는 방식
- [references/verification-notes.md](references/verification-notes.md): state/effect/event integration 검증 기준
