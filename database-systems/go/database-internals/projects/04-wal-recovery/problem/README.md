# Problem Guide

이 문서는 04 WAL Recovery 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다.
- 레코드는 checksum, type, key/value 길이, payload를 포함해야 합니다.
- replay는 첫 손상 레코드에서 멈추고 그 뒤는 버려야 합니다.
- flush 후에는 기존 WAL을 제거하거나 회전하고 새 active WAL을 열어야 합니다.

## 이번 범위에서 일부러 뺀 것

- group commit, fsync batching, 압축 로그 세그먼트는 포함하지 않습니다.
- 복수 writer와 distributed recovery는 다루지 않습니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: WAL Recovery
- 원래 구현 형태: JavaScript 기반 durability 과제로, WAL append와 replay 로직을 중심으로 구성돼 있었습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 WAL 단독 구현에 더해 store integration과 post-flush rotation을 함께 검증하도록 확장했습니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
