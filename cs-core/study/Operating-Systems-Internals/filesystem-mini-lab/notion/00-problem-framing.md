# 00 Problem Framing

## 문제를 어떻게 이해했는가

이 프로젝트는 “filesystem을 만든다”보다 “inode, block, journal이 최소 단위에서 어떻게 연결되는지 설명한다”에 가깝다. 그래서 nested directory나 권한 모델보다 allocation과 recovery를 먼저 보이는 구조를 우선했다.

## 저장소 기준 성공 조건

- `mkfs`, `create`, `write`, `cat`, `ls`, `unlink`, `recover`가 한 이미지 위에서 일관되게 동작한다.
- inode bitmap과 block bitmap이 실제 상태를 반영한다.
- reopen 뒤에도 상태가 유지된다.
- prepared entry discard와 committed entry replay가 테스트로 남는다.

## 고정 범위

- root-only filesystem
- metadata-only journal
- JSON disk image
- single-file whole-write model

## 제외 범위

- nested directory
- permission bit
- rename
- concurrent access
