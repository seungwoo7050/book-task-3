# Docs Guide

이 디렉터리는 08 Failure-Injected Log Replication을 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/failure-injection-harness.md`](concepts/failure-injection-harness.md): drop, duplicate, pause를 어떤 관찰 질문으로 연결하는지 설명합니다.
- [`concepts/quorum-commit-and-retry.md`](concepts/quorum-commit-and-retry.md): quorum commit과 follower retry가 어떻게 같이 움직이는지 설명합니다.

## 추천 읽기 순서

1. `failure-injection-harness.md`를 읽으며 네트워크 하네스가 어떤 메시지를 흔드는지 확인합니다.
2. `quorum-commit-and-retry.md`를 읽으며 commit index와 catch-up 관계를 잡습니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 drop, duplicate, pause가 각각 어떤 시나리오에서 쓰이는지 연결합니다.
