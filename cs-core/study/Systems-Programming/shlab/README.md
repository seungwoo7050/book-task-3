# Shell Lab

## 이 프로젝트가 가르치는 것

`shlab`은 프로세스 그룹, foreground/background job control, `SIGCHLD` 처리, `fork` 주변 race를 실제 셸 구현으로 익히게 합니다.
겉보기에는 작은 셸이지만, 운영체제 수업에서 자주 헷갈리는 동기화와 시그널 전달 규칙을 압축해서 보여 줍니다.

## 누구를 위한 문서인가

- 작은 셸을 직접 구현하며 process control을 체득하고 싶은 학습자
- 시그널과 job list race를 공개 저장소에서 설명하는 방법이 필요한 사람
- 공식 starter 없이도 과제 계약을 어떻게 보존할지 보고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`c/README.md`](c/README.md)
3. [`cpp/README.md`](cpp/README.md)
4. [`docs/README.md`](docs/README.md)
5. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
shlab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
  tests/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

문제 경계 확인:

```bash
cd problem
make status
```

C 구현 검증:

```bash
cd c
make clean && make test
```

C++ 구현 검증:

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- 공개 문서는 process group, signal forwarding, race discipline을 설명합니다.
- 공식 starter shell과 공식 traces는 공개 트리에 싣지 않습니다.
- 대신 `tests/`, `c/tests/`, `cpp/tests/`의 self-owned 검증 경로를 중심으로 문서를 구성합니다.

## 포트폴리오로 확장하는 힌트

- 이 프로젝트는 "왜 마스킹이 필요한가"를 설명할 수 있을 때 강해집니다.
- 개인 저장소에서는 `fork` 직후와 `SIGCHLD` 도착 사이의 race를 타임라인 그림으로 정리하면 좋습니다.
