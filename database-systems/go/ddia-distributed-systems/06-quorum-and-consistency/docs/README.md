# Docs Guide

이 디렉터리는 06 Quorum and Consistency를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/quorum-read-write.md`](concepts/quorum-read-write.md): `W + R > N`이 어떤 의미인지 설명합니다.
- [`concepts/versioned-register.md`](concepts/versioned-register.md): single-version register에서 read merge가 어떻게 동작하는지 설명합니다.

## 추천 읽기 순서

1. `quorum-read-write.md`를 읽으며 quorum 조건이 왜 필요한지 잡습니다.
2. `versioned-register.md`를 읽으며 read가 어떤 정보를 비교하는지 확인합니다.
3. [`references/README.md`](references/README.md)로 어떤 자료를 참고해 문서를 구성했는지 확인합니다.
4. 구현과 테스트를 읽으며 stale read가 정확히 어떤 fixture에서 재현되는지 연결합니다.
