# Docs Guide

이 디렉터리는 01 MemTable SkipList를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/skiplist-invariants.md`](concepts/skiplist-invariants.md): 정렬된 계층 구조가 삽입·조회·순회 요구를 어떻게 동시에 만족시키는지 설명합니다.

## 추천 읽기 순서

1. `skiplist-invariants.md`를 읽으며 핵심 용어를 맞춥니다.
2. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
3. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
