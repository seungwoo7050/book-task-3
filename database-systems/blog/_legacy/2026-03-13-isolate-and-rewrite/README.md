# Blog Index

`database-systems/`의 README가 무엇을 만들었는지 보여 주는 표면이라면, 이 `blog/`는 코드와 재검증 CLI를 바탕으로 실제 판단 이동을 다시 세우는 계층이다.

## 이 계층에서 고정한 원칙

- 단위는 `독립 프로젝트`다. 트랙 전체 회고문으로 쓰지 않는다.
- 기존 초안은 `_legacy/`로 격리하고, 새 초안은 소스와 실행 흔적으로만 다시 쓴다.
- 근거는 `src/internal`, `tests`, `README/problem/docs`, 재검증 CLI만 사용한다.
- 최종 시리즈는 `00 -> 10 -> 20 -> 30` 순서로 읽되, 내부 작업 산출물로 `_evidence-ledger.md`와 `_structure-outline.md`를 함께 남긴다.

## 현재 범위

- [Python Blog Index](python/README.md)
- [Go Blog Index](go/README.md)

## 권장 읽기 흐름

1. `../README.md`에서 프로젝트 맥락을 잡는다.
2. 언어별 blog index에서 트랙을 고른다.
3. 각 프로젝트의 `00-series-map.md`에서 질문과 재검증 명령을 확인한다.
4. `10 -> 20 -> 30` chronology로 실제 판단 이동을 따라간다.
