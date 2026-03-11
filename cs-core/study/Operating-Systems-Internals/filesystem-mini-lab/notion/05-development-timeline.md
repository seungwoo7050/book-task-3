# 05 Development Timeline

## 재구축 순서

```bash
cd cs-core/study/Operating-Systems-Internals/filesystem-mini-lab/problem
make test
make run-demo
```

## 2026-03-11 재검증 기록

- `make test` 결과: `5 passed`
- `make run-demo` 결과:
  - `note` 생성 후 `hello-os` 출력 확인
  - `after_commit` crash 재현
  - `recover` 결과 `replayed=1 discarded=0`

## 읽는 순서 메모

1. `problem/README.md`로 범위를 다시 잡는다.
2. `docs/`에서 inode/block/journal 용어를 맞춘다.
3. `tests/`를 읽어 persistence와 recovery 계약을 확인한다.
4. demo를 실행해 image 상태와 recovery 출력 shape를 눈으로 본다.
