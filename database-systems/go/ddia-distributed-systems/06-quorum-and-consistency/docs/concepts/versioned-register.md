# Versioned Register

이 프로젝트의 value는 `(version, data)` 두 값으로만 구성됩니다. vector clock처럼 여러 branch를 추적하지 않고, 가장 큰 version 하나만 최신으로 취급합니다.

## 왜 version이 필요한가

replica마다 같은 key의 상태가 다를 수 있기 때문입니다. read가 여러 replica를 동시에 보면 “어느 값이 더 최신인가”를 비교할 기준이 필요합니다.

## 이 구현의 규칙

- write quorum이 성공하면 cluster-level version이 1 증가합니다.
- 성공한 write는 현재 살아 있는 replica에만 전파됩니다.
- read는 responder 집합 안에서 가장 높은 version을 선택합니다.

## 여기서 다루지 않는 것

- concurrent write conflict 해결
- vector clock 기반 sibling merge
- last-write-wins timestamp 비교

이 제한 덕분에 학습자는 quorum overlap과 stale read 질문에만 집중할 수 있습니다.
