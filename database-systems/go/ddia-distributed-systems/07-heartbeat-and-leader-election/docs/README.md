# Docs Guide

이 디렉터리는 07 Heartbeat and Leader Election을 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/heartbeat-failure-detector.md`](concepts/heartbeat-failure-detector.md): heartbeat silence가 suspicion으로 바뀌는 과정을 설명합니다.
- [`concepts/majority-election.md`](concepts/majority-election.md): 왜 majority vote가 split-brain을 막는지 설명합니다.

## 추천 읽기 순서

1. `heartbeat-failure-detector.md`를 읽으며 failure signal이 어떻게 생기는지 맞춥니다.
2. `majority-election.md`를 읽으며 leader authority가 어떤 조건으로 바뀌는지 확인합니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 suspicion, failover, step-down이 어디서 일어나는지 연결합니다.
