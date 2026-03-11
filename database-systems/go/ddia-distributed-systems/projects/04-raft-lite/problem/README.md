# Problem Guide

이 문서는 04 Raft Lite 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- leader election과 단일 leader 보장을 재현해야 합니다.
- up-to-date log vote rule을 구현해야 합니다.
- AppendEntries consistency check가 필요합니다.
- majority replicated entry만 commit해야 합니다.
- higher term 발견 시 leader가 step-down해야 합니다.

## 이번 범위에서 일부러 뺀 것

- production-grade persistence, membership change, snapshotting은 포함하지 않습니다.
- 실제 네트워크 transport와 disk-backed log는 후속 확장으로 남깁니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: Consensus / Raft
- 원래 구현 형태: JavaScript 기반 distributed-cluster 과제로, 작은 tick 기반 consensus 시뮬레이터 형태였습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 Go 전체 분산 트랙의 심화 슬롯으로 두어, Python 입문 트랙과 분명히 구분된 합의 학습 지점을 만듭니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
