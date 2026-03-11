# Docs Guide

이 디렉터리는 01 RPC Framing를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/frame-boundary.md`](concepts/frame-boundary.md): TCP stream 위에서 message boundary를 복구하는 기본 원리를 설명합니다.
- [`concepts/pending-map.md`](concepts/pending-map.md): correlation id와 pending call map이 동시 요청을 어떻게 구분하는지 정리합니다.

## 추천 읽기 순서

1. `frame-boundary.md`를 읽으며 핵심 용어를 맞춥니다.
2. `pending-map.md`를 읽으며 핵심 용어를 맞춥니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 위 개념이 코드에서 어디에 드러나는지 연결합니다.
