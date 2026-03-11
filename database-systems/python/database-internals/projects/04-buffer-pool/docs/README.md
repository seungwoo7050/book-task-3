# Docs Guide

이 디렉터리는 04 Buffer Pool를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/lru-eviction.md`](concepts/lru-eviction.md): LRU 교체 정책이 buffer pool hit ratio에 어떤 영향을 주는지 설명합니다.
- [`concepts/pin-and-dirty.md`](concepts/pin-and-dirty.md): pin count와 dirty write-back이 eviction 정책과 어떻게 충돌하는지 정리합니다.

## 추천 읽기 순서

1. `lru-eviction.md`를 읽으며 핵심 용어를 맞춥니다.
2. `pin-and-dirty.md`를 읽으며 핵심 용어를 맞춥니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
