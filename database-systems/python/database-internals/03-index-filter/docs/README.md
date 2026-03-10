# Docs Guide

이 디렉터리는 03 Index Filter를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/bloom-filter-sizing.md`](concepts/bloom-filter-sizing.md): Bloom filter의 bit budget과 false positive trade-off를 설명합니다.
- [`concepts/sparse-index-scan.md`](concepts/sparse-index-scan.md): sparse index가 전체 스캔을 작은 block scan으로 줄이는 과정을 정리합니다.

## 추천 읽기 순서

1. `bloom-filter-sizing.md`를 읽으며 핵심 용어를 맞춥니다.
2. `sparse-index-scan.md`를 읽으며 핵심 용어를 맞춥니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
