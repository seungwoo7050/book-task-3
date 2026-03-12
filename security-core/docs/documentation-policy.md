# 문서 정책

## 목적

이 레포의 문서는 “보안 구현이 있다”보다 “문제, 해답, 검증 근거를 30초 안에 찾을 수 있다”를 우선합니다. 모든 설명은 재현 가능한 명령, 실제 fixture, 현재 상태를 중심으로 유지합니다.

## 기본 원칙

- 설명 문장은 한국어를 기본으로 쓰고, 명령어·경로·도구명·패키지명·식별자·action key는 영어 원문을 유지합니다.
- 루트와 프로젝트 README는 모두 `문제 / 내가 만든 답 / 검증` 관점을 먼저 드러냅니다.
- 구현이 없는 planned 항목은 표나 문장으로만 남기고, 빈 디렉터리나 빈 링크는 만들지 않습니다.
- 과장 표현보다 현재 검증 범위와 의도적 제외 범위를 분명히 적습니다.

## README 계약

- 루트 `README.md`: `이 레포가 푸는 문제`, `이 레포의 답`, `추천 읽기 순서`, `빠른 검증`, `프로젝트 카탈로그`
- 프로젝트 `README.md`: `이 프로젝트의 문제`, `내가 만든 답`, `검증 명령`, `입출력 계약`, `읽는 순서`, `배운 점과 한계`
- `problem/README.md`: 문제, 성공 기준, canonical validation, schema 또는 fixture, provenance
- `python/README.md`: 구현 개요, 핵심 모듈, CLI 계약, 테스트 범위
- `docs/README.md`: 개념 문서 지도와 공용 가이드 링크
- `notion/README.md`: 현재판 학습 노트 묶음과 추천 읽기 순서

세부 형식은 [readme-contract.md](readme-contract.md)에서 관리합니다.

## notion 규칙

- `notion/`은 현재 공개용 학습 노트입니다.
- 기본 세트는 `README.md`, `00-problem-framing.md`, `01-approach-log.md`, `02-debug-log.md`, `03-retrospective.md`, `04-knowledge-index.md`, `05-development-timeline.md`입니다.
- `05-development-timeline.md`는 새 환경에서 다시 실행할 수 있는 명령 순서와 성공 신호를 우선 기록합니다.
- 노트를 전면 개정할 때는 기존 내용을 `notion-archive/`로 이동하고 현재판을 다시 만듭니다.

## 검증 기록 규칙

- 프로젝트 README와 `problem/README.md`에는 canonical 검증 명령과 대표 demo/replay 명령을 모두 남깁니다.
- 테스트가 보장하는 사실과 문서 수준의 가정은 분리해서 씁니다.
- reference vector, scenario bundle, advisory bundle 같은 입력의 출처는 `problem/README.md`와 `docs/references/README.md`에 남깁니다.
