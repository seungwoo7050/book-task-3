# README Contract

이 저장소의 README는 GitHub 첫 화면에서 `무슨 문제를 풀었는가`, `답이 어디 있는가`, `어떻게 검증하는가`를 바로 찾게 하는 공개 표면이다. 긴 reasoning과 작업 기록은 `docs/`와 `notion/`으로 내리고, README는 길 찾기 계약을 유지한다.

## 루트 README

- 저장소가 다루는 문제군
- 단계별 학습 순서
- 전체 프로젝트 카탈로그
- 대표 검증 명령
- 문서 지도

## `study/README.md`

- 단계 인덱스
- 읽는 순서
- 각 단계 README로 내려가는 링크

## 단계 README

- 단계의 핵심 질문 한 줄 요약
- 프로젝트 카탈로그 표
- 공통 읽기 순서

## 프로젝트 README

- `문제가 뭐였나`
- `제공된 자료`
- `이 레포의 답`
- `어떻게 검증하나`
- `무엇을 배웠나`
- `현재 한계`

## 하위 README

- `python/README.md`, `cpp/README.md`, `analysis/README.md`, `docs/README.md`는 모두 `이 폴더의 역할`, `먼저 볼 파일`, `기준 명령`, `현재 범위`, `남은 약점`만 보여 준다.
- `notion/README.md`는 공개 노트의 인덱스이지만 프로젝트 이해의 엔트리포인트가 아니다.

## 언어 정책

- explanatory prose와 authored code comment는 한국어를 기본으로 한다.
- 명령어, file path, protocol name, RFC 용어, code identifier, literal request/response, error string은 원문 English를 유지한다.
