# Problem Guide

이 문서는 06 Index Filter 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- Bloom filter를 직렬화·복원할 수 있어야 합니다.
- 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다.
- footer metadata를 읽어 filter와 index 위치를 복원해야 합니다.
- lookup 시 bloom reject와 bounded block scan이 둘 다 드러나야 합니다.

## 이번 범위에서 일부러 뺀 것

- learned index와 adaptive filter는 포함하지 않습니다.
- range query 최적화와 block cache 연동은 다음 단계 확장으로 남깁니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: Index and Filter Optimization
- 원래 구현 형태: JavaScript 기반 storage-engine 최적화 과제로, Bloom filter와 sparse index가 분리돼 있었습니다.
- 현재 프로젝트에서의 재구성: 현재 레포에서는 둘을 하나의 SSTable open path 안으로 통합해 read-path 최적화 흐름을 더 자연스럽게 설명합니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
