# Shell Lab starter trace 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 공식 starter traces를 공개 트리에서 제거한 이유와 대체 검증 경로를 설명합니다.

## 누구를 위한 문서인가

- trace 파일이 왜 없는지 알고 싶은 사람
- self-owned 테스트 경로를 찾고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`../../tests/direct_shell_case.sh`](../../tests/direct_shell_case.sh)
3. [`../../c/tests/run_tests.sh`](../../c/tests/run_tests.sh)
4. [`../../cpp/tests/run_tests.sh`](../../cpp/tests/run_tests.sh)

## 디렉터리 구조

```text
data/
  README.md
```

## 검증 방법

- 공식 starter trace 대신 self-owned 테스트 스크립트를 사용합니다.
- 실제 실행은 구현 디렉터리의 `make test`를 따릅니다.

## 스포일러 경계

- 제거된 공식 trace는 공개하지 않습니다.
- README는 대체 테스트 위치만 설명합니다.

## 포트폴리오로 확장하는 힌트

- 공식 테스트 자산을 못 싣는 경우, 대체 테스트 전략을 명시하는 것만으로도 프로젝트 설계가 좋아집니다.
