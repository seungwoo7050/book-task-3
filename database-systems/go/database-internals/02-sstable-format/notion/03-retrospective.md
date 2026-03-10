# 회고

## 이번 단계에서 명확해진 것
- 정렬된 in-memory 상태를 immutable file contract로 굳히는 순간부터 storage layer 설명이 훨씬 명확해집니다.
- index와 footer만으로도 꽤 설득력 있는 point lookup path를 만들 수 있습니다.
- 파일 포맷 단계에서도 tombstone semantics를 보존해야 상위 계층의 read precedence가 단순해집니다.

## 아직 단순화한 부분
- block-level checksum과 corruption detection은 아직 없습니다.
- read amplification을 줄이는 sparse index나 bloom filter는 포함하지 않았습니다.

## 다음에 확장한다면
- block checksum과 corruption recovery policy를 넣어 durability 설명을 강화할 수 있습니다.
- sparse index와 bloom filter를 추가해 point lookup 최적화 단계를 이어갈 수 있습니다.

## `03 Mini LSM Store`로 넘길 질문
- mutable memtable과 immutable SSTable 사이 flush handoff는 어떤 순서로 일어나야 하는가?
- 겹치는 SSTable이 여러 장 생기면 최신 값을 어떤 순서로 선택할 것인가?
