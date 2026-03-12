# README Contract

이 문서는 `security-core`의 공개 표면이 어떤 순서로 정보를 드러내야 하는지 정리한 계약서입니다.

## 루트 README

루트 `README.md`는 아래 순서를 유지합니다.

1. `이 레포가 푸는 문제`
2. `이 레포의 답`
3. `추천 읽기 순서`
4. `빠른 검증`
5. `프로젝트 카탈로그`

루트 README는 저장소 전체를 설명하는 곳이지, 각 프로젝트의 긴 배경 설명을 붙이는 곳이 아닙니다.

## 프로젝트 README

각 프로젝트 `README.md`는 아래 순서를 유지합니다.

1. `이 프로젝트의 문제`
2. `내가 만든 답`
3. `검증 명령`
4. `입출력 계약`
5. `읽는 순서`
6. `배운 점과 한계`

첫 화면에서 문제와 해답이 먼저 보여야 하므로, “왜 배우는가”나 “한줄 소개”는 별도 섹션으로 두지 않습니다.

## 하위 README 역할

- `problem/README.md`: 문제 정의, 성공 기준, canonical validation, fixture/provenance
- `docs/README.md`: 개념 문서 지도와 참고 문서 링크
- `python/README.md`: 구현 개요, 핵심 모듈, CLI 계약, 테스트
- `notion/README.md`: 현재판 학습 노트 묶음과 추천 읽기 순서

## 언어 규칙

- 설명 문장은 한국어를 기본으로 씁니다.
- 경로, 명령어, control ID, priority, action key, 코드 식별자는 영어로 유지합니다.
- 실행 결과물도 사람에게 읽히는 제목과 문장은 한국어로 맞추고, machine-facing key는 바꾸지 않습니다.
