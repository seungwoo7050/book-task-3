# 개념 문서 안내

이 디렉터리는 `static-type-checking`을 읽기 전에 핵심 타입 개념을 짧게 맞추는 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/static-vs-runtime-errors.md`](concepts/static-vs-runtime-errors.md): 어떤 오류를 checker가 맡고, 어떤 오류를 runtime에 남기는지 설명합니다.
- [`concepts/type-environment.md`](concepts/type-environment.md): lexical environment와 별개로 type environment가 왜 필요한지 정리합니다.
- [`concepts/function-type-checking.md`](concepts/function-type-checking.md): parameter, return, call boundary를 어떤 규칙으로 검사하는지 설명합니다.

## 추천 읽기 순서

1. static/runtime error 메모로 책임 경계를 먼저 맞춥니다.
2. type environment 메모로 이름이 "값"이 아니라 "타입"으로 해석되는 경로를 확인합니다.
3. function checking 메모로 higher-order function까지 어떤 방식으로 검사하는지 읽습니다.
4. [`references/README.md`](references/README.md)로 provenance를 확인합니다.
