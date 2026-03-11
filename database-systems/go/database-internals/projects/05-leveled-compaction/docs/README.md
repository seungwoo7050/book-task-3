# Docs Guide

이 디렉터리는 05 Leveled Compaction를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/merge-ordering.md`](concepts/merge-ordering.md): newest-first 우선순위를 보존한 k-way merge가 tombstone 처리와 어떻게 연결되는지 정리합니다.
- [`concepts/manifest-atomicity.md`](concepts/manifest-atomicity.md): compaction 결과 파일과 manifest가 어긋나지 않도록 쓰는 방법을 설명합니다.

## 추천 읽기 순서

1. `merge-ordering.md`를 읽으며 핵심 용어를 맞춥니다.
2. `manifest-atomicity.md`를 읽으며 핵심 용어를 맞춥니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
