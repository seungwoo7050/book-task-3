# Docs Guide

이 디렉터리는 04 Clustered KV Capstone를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/static-topology.md`](concepts/static-topology.md): capstone에서 정적 shard topology와 정적 leader 배치를 택한 이유를 설명합니다.
- [`concepts/replicated-write-pipeline.md`](concepts/replicated-write-pipeline.md): router, leader, follower, disk-backed store가 한 요청 안에서 어떻게 이어지는지 설명합니다.

## 추천 읽기 순서

1. `static-topology.md`를 읽으며 핵심 용어를 맞춥니다.
2. `replicated-write-pipeline.md`를 읽으며 핵심 용어를 맞춥니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
