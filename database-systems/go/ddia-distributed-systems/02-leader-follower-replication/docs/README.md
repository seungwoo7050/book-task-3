# Docs Guide

이 디렉터리는 02 Leader-Follower Replication를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/log-shipping.md`](concepts/log-shipping.md): leader log를 follower가 watermark 이후부터 따라가는 방식을 설명합니다.
- [`concepts/idempotent-follower.md`](concepts/idempotent-follower.md): 같은 entry를 다시 받아도 follower state가 깨지지 않는 이유를 정리합니다.

## 추천 읽기 순서

1. `log-shipping.md`를 읽으며 핵심 용어를 맞춥니다.
2. `idempotent-follower.md`를 읽으며 핵심 용어를 맞춥니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
