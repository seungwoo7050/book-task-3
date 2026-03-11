# Synchronization Contention Lab 노트

## 목적

이 디렉터리는 `synchronization-contention-lab`의 현재 공개용 학습 노트다. 공개 README가 시나리오 안내문이라면, 이 폴더는 invariant 선택 이유와 재검증 절차를 압축한 현재판이다.

## 이 버전에서 다루는 것

- 왜 counter, gate, buffer를 각각 다른 primitive 예제로 골랐는지
- timing보다 invariant를 먼저 테스트로 고정한 이유
- macOS 환경에서 semaphore 구현을 어떻게 맞췄는지
- 2026-03-11 기준 shell test와 demo 재검증 결과

## 권장 읽기 순서

1. `00-problem-framing.md`
2. `05-development-timeline.md`
3. `01-approach-log.md`
4. `02-debug-log.md`
5. `04-knowledge-index.md`
6. `03-retrospective.md`

## 메모

- 현재 프로젝트는 `notion/`만으로 재학습과 재검증이 가능하도록 유지한다.
- 추가 백업은 로컬에서만 관리한다.
