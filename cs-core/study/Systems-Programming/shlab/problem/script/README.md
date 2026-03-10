# Shell Lab starter driver 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 제거된 starter driver 대신 어떤 self-owned 검증 하네스를 쓰는지 설명합니다.

## 누구를 위한 문서인가

- 기존 Perl driver 대신 무엇을 실행해야 하는지 알고 싶은 사람
- 공개 저장소에서 테스트 자동화를 어떻게 대체했는지 보고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`../../tests/`](../../tests/)
3. [`../../c/tests/run_tests.sh`](../../c/tests/run_tests.sh)
4. [`../../cpp/tests/run_tests.sh`](../../cpp/tests/run_tests.sh)

## 디렉터리 구조

```text
script/
  README.md
```

## 검증 방법

- 직접 실행 가능한 검증은 `../../tests/`, `../../c/tests/`, `../../cpp/tests/` 아래에 있습니다.
- 공식 starter driver는 공개 트리에 포함하지 않습니다.

## 스포일러 경계

- 제거된 driver 자체는 공개하지 않습니다.
- README는 대체 하네스 위치만 안내합니다.

## 포트폴리오로 확장하는 힌트

- 외부 driver를 못 싣는 경우, 직접 만든 테스트 흐름을 README로 명시하면 충분히 설득력이 있습니다.
