# Filesystem Mini Lab 시리즈 맵

`filesystem-mini-lab`은 root-only toy filesystem으로 inode allocation, block allocation, metadata journaling, recovery를 작은 JSON disk image 위에서 설명하는 실험이다. 이 시리즈는 결과만 정리해 둔 회고문이 아니라, inode/block allocator를 먼저 세운 뒤 journal prepare/commit/apply/recover가 왜 별도 단계여야 하는지 따라간다.를 끝까지 따라가게 만드는 입구다.

2026-03-13에 기존 초안을 `study/blog/_legacy/2026-03-13-isolate-and-rewrite/Operating-Systems-Internals/filesystem-mini-lab/`로 옮긴 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 시리즈를 다시 썼다. 그래서 이 문서는 '무엇을 만들었는가'보다 '어떤 순서로 읽어야 그 판단 이동이 보이는가'를 먼저 설명한다.

## 이 시리즈를 읽는 방법

가장 먼저 `01-evidence-ledger.md`에서 살아 있는 근거를 모아 본다. 그 다음 `_structure-outline.md`에서 왜 최종 글이 그 순서로 배치되는지 확인한다. 마지막으로 `10-2026-03-13-reconstructed-development-log.md`에서 그 근거가 실제 서사로 어떻게 이어지는지 읽는다.

## 이번 재작성에서 붙잡은 source-of-truth

- 문제 계약: [`README.md`](../../../Operating-Systems-Internals/filesystem-mini-lab/README.md), [`problem/README.md`](../../../Operating-Systems-Internals/filesystem-mini-lab/problem/README.md)
- 구현 표면: `python/src/os_mini_fs/__init__.py`, `python/src/os_mini_fs/__main__.py`, `python/src/os_mini_fs/cli.py`, `python/src/os_mini_fs/core.py`
- 검증 entrypoint: `make test && make run-demo` in `problem`
- 개념 축: `inode and blocks`, `journaling recovery`, `transaction states`

## 읽는 순서

1. [`01-evidence-ledger.md`](01-evidence-ledger.md) — source-first 근거와 phase별 판단 전환점을 먼저 모아 둔 문서
2. [`_structure-outline.md`](_structure-outline.md) — 최종 글의 읽기 곡선과 장면 배치를 설명하는 편집 설계 메모
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md) — 구현 순서, 코드, CLI를 한 흐름으로 다시 쓴 최종 blog

## 이번에 따라간 질문

inode/block allocator를 먼저 세운 뒤 journal prepare/commit/apply/recover가 왜 별도 단계여야 하는지 따라간다.
