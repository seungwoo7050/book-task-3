# Filesystem Mini Lab 노트

## 목적

이 디렉터리는 `filesystem-mini-lab`의 현재 공개용 학습 노트다. 공개 README가 탐색용이라면, 이 폴더는 “왜 JSON image 하나로도 journaling을 설명할 수 있는가”와 “crash recovery를 어떤 순서로 다시 확인할 것인가”를 압축한다.

## 이 버전에서 다루는 것

- root-only 제약을 둔 이유
- inode/block allocation과 journal 상태를 어떻게 분리했는지
- prepared discard와 committed replay가 각각 무엇을 보장하는지
- 2026-03-11 기준 재검증 절차

## 권장 읽기 순서

1. `00-problem-framing.md`
2. `05-development-timeline.md`
3. `01-approach-log.md`
4. `02-debug-log.md`
5. `04-knowledge-index.md`
6. `03-retrospective.md`

## 메모

- 현재 프로젝트는 `notion/`만으로 재학습과 재검증이 가능하도록 유지한다.
- 별도 백업이 필요하면 로컬에서만 관리한다.
