# Filesystem Mini Lab

## 이 프로젝트가 가르치는 것

`filesystem-mini-lab`는 root-only toy filesystem을 통해 inode allocation, block allocation, metadata journaling, recovery를 작은 JSON disk image 위에서 설명하는 실험이다.

## 누구를 위한 문서인가

- inode와 block bitmap을 직접 만져 보고 싶은 학습자
- journaling이 recovery에 어떤 도움을 주는지 작은 예제로 보고 싶은 사람
- 복잡한 커널 파일시스템 전에 최소 모델을 먼저 잡고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`python/README.md`](python/README.md)
3. [`docs/README.md`](docs/README.md)
4. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
filesystem-mini-lab/
  README.md
  problem/
  python/
  docs/
  notion/
```

## 검증 방법

```bash
cd problem
make test
make run-demo
```

검증에서 보는 핵심 신호:

- create/write/read/delete가 이미지 하나에서 일관되게 동작한다.
- reopen 뒤에도 파일 내용이 유지된다.
- `after_prepare`와 `after_commit` crash가 recovery에서 다르게 처리된다.

## 스포일러 경계

- nested directory, permission bit, hard link, journaling mode 비교는 다루지 않는다.
- README는 문제 범위와 검증 경로에 집중하고, 긴 설명은 `docs/`와 `notion/`으로 분리한다.

## 포트폴리오로 확장하는 힌트

- root-only 제약을 걷어내고 subdirectory path lookup을 추가하면 한 단계 더 현실적인 toy filesystem이 된다.
- metadata-only journaling 뒤에 data journaling 또는 copy-on-write를 비교해도 좋다.

## 현재 한계

- whole-file write만 지원하고 offset write는 다루지 않는다.
- root-only 모델이라 path traversal 복잡도는 설명하지 않는다.
