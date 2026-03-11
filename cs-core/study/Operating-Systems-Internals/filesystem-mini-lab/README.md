# Filesystem Mini Lab

`filesystem-mini-lab`은 root-only toy filesystem으로 inode allocation, block allocation, metadata journaling, recovery를 작은 JSON disk image 위에서 설명하는 실험이다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| 작은 filesystem 모델에서 create/write/read/delete와 journaling recovery를 구현한다. | root-only 모델, whole-file write, metadata journaling에 범위를 고정하고 subdirectory와 permission은 다루지 않는다. | 구현은 [`python/`](python/README.md)의 filesystem 모델, JSON disk image, crash-recovery demo로 정리한다. | [`problem/README.md`](problem/README.md), [`python/README.md`](python/README.md) | inode/block allocation, journaling, recovery, disk image 모델링 | `public verified` |

## 디렉터리 역할

- `problem/`: 문제 범위와 canonical `make` entrypoint
- `python/`: filesystem 구현과 CLI
- `docs/`: inode, block, transaction state, journaling recovery 정리
- `notion/`: 실패 사례와 재검증 기록

## 검증 빠른 시작

```bash
cd problem
make test
make run-demo
```

검증에서 보는 핵심 신호:

- create/write/read/delete가 이미지 하나에서 일관되게 동작한다.
- reopen 뒤에도 파일 내용이 유지된다.
- `after_prepare`와 `after_commit` crash가 recovery에서 다르게 처리된다.

## 공개 경계

- nested directory, permission bit, hard link, journaling mode 비교는 다루지 않는다.
- README는 문제 범위와 검증 경로에 집중하고, 긴 설명은 `docs/`와 `notion/`으로 분리한다.

## 현재 한계

- whole-file write만 지원하고 offset write는 다루지 않는다.
- root-only 모델이라 path traversal 복잡도는 설명하지 않는다.
