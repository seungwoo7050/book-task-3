# Virtual Memory Lab 노트

## 목적

이 디렉터리는 `virtual-memory-lab`의 현재 공개용 학습 노트다. 공개 README가 탐색용 안내문이라면, 이 폴더는 trace 선택 이유, replacement rule 해석, 재검증 절차를 압축한 현재판이다.

## 이 버전에서 다루는 것

- anomaly/locality/dirty eviction trace를 왜 따로 뒀는지
- FIFO, LRU, Clock, OPT를 어떤 비교 기준으로 읽는지
- replay에서 frame index 대신 page set을 보이게 한 이유
- 2026-03-11 기준 재검증 기록

## 권장 읽기 순서

1. `00-problem-framing.md`
2. `05-development-timeline.md`
3. `01-approach-log.md`
4. `02-debug-log.md`
5. `04-knowledge-index.md`
6. `03-retrospective.md`

## 메모

- 현재 프로젝트는 `notion/`만으로 재학습과 재검증이 가능하도록 유지한다.
- 추가 백업은 로컬에서만 두고, 공개 표면에는 포함하지 않는다.
