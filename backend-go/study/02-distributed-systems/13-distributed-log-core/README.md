# 13 Distributed Log Core

## 한 줄 요약

append-only store, mmap index, segment rotation, log abstraction을 직접 구현해 commit log 핵심을 익히는 대표 과제다.

## 이 프로젝트가 푸는 문제

- length-prefixed store와 fixed-width index를 직접 구현해야 한다.
- segment rotation과 log abstraction을 구성해야 한다.
- 파일 정리와 reopen 시나리오까지 테스트로 다뤄야 한다.

## 내가 만든 답

- store, index, segment, log core를 `solution/go`에 구현했다.
- mmap index와 segment rotation을 테스트 및 benchmark와 함께 정리했다.
- replication layer는 의도적으로 제외하고 log core에 집중했다.

## 핵심 설계 선택

- Kafka형 시스템을 한 번에 복제하지 않고 append-only log 핵심 구조만 분리했다.
- 파일 포맷과 segment lifecycle을 먼저 구현해 분산 복제 이전의 로컬 불변식을 학습하게 했다.

## 검증

- `cd solution/go && go test ./log/... -bench=.`
- `make -C problem test`
- `make -C problem bench`

## 제외 범위

- replication
- cluster coordination

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/02-distributed-system/05-distributed-log (`legacy/02-distributed-system/05-distributed-log/README.md`, public repo에는 미포함)
