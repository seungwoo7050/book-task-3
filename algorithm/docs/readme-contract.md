# README Contract

이 저장소의 README는 GitHub 첫 화면에서 `무슨 문제를 풀었는가`, `이 레포의 답이 어디 있는가`, `어떻게 검증하는가`, `더 긴 노트는 어디에 있는가`를 바로 찾게 하는 공개 표면이다. 긴 reasoning과 디버깅 이력은 `docs/`와 `notion/`으로 내리고, README는 길찾기 계약을 유지한다.

## 루트 README
- 저장소가 다루는 문제군
- 16개 트랙 인덱스와 대표 문제
- 대표 검증 명령과 검증 문서 위치
- 전체 카탈로그와 커리큘럼 문서 링크

## `study/README.md`
- 트랙 인덱스
- 각 트랙의 핵심 질문
- 대표 문제, 답 위치, 대표 검증, 상태

## 트랙 README
- `트랙 한 줄 질문`
- `왜 이 순서인가`
- `프로젝트 카탈로그 표`
- `공통 읽기 순서`
- `포트폴리오 관점 메모`

## 프로젝트 README
- 상단 상태 표: `상태`, `문제 배경`, `정식 검증`
- 본문 6문답: `문제가 뭐였나`, `제공된 자료`, `이 레포의 답`, `어떻게 검증하나`, `무엇을 배웠나`, `현재 한계`

## 하위 README
- `problem/README.md`: 이 폴더의 역할, 제공된 자료, 기준 명령, 문제 계약, 남은 약점
- `python/README.md`, `cpp/README.md`: 이 폴더의 역할, 먼저 볼 파일, 기준 명령, 현재 범위, 남은 약점
- `docs/README.md`: 이 폴더의 역할, 먼저 볼 파일, 기준 명령, 현재 범위, 남은 약점
- `notion/README.md`: 공개 노트 인덱스와 읽는 순서만 보여 주며, 프로젝트 엔트리포인트 역할은 하지 않는다.

## 언어 정책
- 설명 문장과 authored code comment는 한국어를 기본으로 쓴다.
- 명령어, 파일 경로, 알고리즘/자료구조 이름, 프로토콜 이름, code identifier, literal output, error string은 English 원문을 유지한다.

## 상태 어휘
- `planned`
- `in-progress`
- `verified`
- `archived`
