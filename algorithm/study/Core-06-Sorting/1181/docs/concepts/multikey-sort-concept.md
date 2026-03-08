# 다중 키 정렬 개념 정리 — 단어 정렬

## 핵심 아이디어
정렬 기준이 복합적일 때 **튜플 키**를 활용.
1차: 길이, 2차: 사전순 → `key=lambda w: (len(w), w)`

## 중복 제거
`set`으로 중복 제거 후 정렬, 또는 `sorted(set(...))`로 한 번에 처리.

## CLRS 연결
CLRS Ch 8.3 Radix Sort에서 다중 키 정렬의 원리(LSD→MSD)를 다룸.
Python의 Timsort는 stable이므로 여러 번 정렬해도 이전 키 순서가 보존된다.
