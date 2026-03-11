# 문서 정책

## 목적

이 레포의 문서는 “보안 코드를 한 번 작성했다”보다 “왜 이 primitive나 방어가 필요한지 설명할 수 있다”를
우선합니다. 모든 문서는 재현 가능한 명령, 고정 fixture, 현재 상태를 중심으로 씁니다.

## 기본 원칙

- 한국어를 기본으로 쓰고, 기술명·도구명·패키지명·CLI 명령·설정 키는 영어 원문을 유지합니다.
- 모든 명령은 `security-core` 레포 루트 기준으로 적습니다.
- 구현이 없는 planned 항목은 설명형 표로만 남기고, 빈 디렉터리나 빈 링크는 만들지 않습니다.
- “production-ready” 같은 과장 표현보다 현재 검증 범위와 제외 범위를 분명히 적습니다.

## README 규칙

프로젝트 `README.md`는 아래 순서를 기본으로 유지합니다.

- 프로젝트 한줄 소개
- 왜 배우는가
- 현재 구현 범위
- 빠른 시작
- 검증 명령
- 먼저 읽을 파일
- 포트폴리오 확장 힌트
- 알려진 한계

`docs/README.md`는 개념 지도 역할을 하고, `notion/README.md`는 현재 학습 노트 묶음을 안내합니다.

## notion 규칙

- `notion/`은 현재 공개용 학습 노트입니다.
- 새 노트는 `README.md`, `00-problem-framing.md`, `01-approach-log.md`, `02-debug-log.md`,
  `03-retrospective.md`, `04-knowledge-index.md`, `05-development-timeline.md`를 기본 세트로 사용합니다.
- `05-development-timeline.md`는 새 환경에서 다시 실행할 수 있는 명령 순서와 성공 신호를 우선 기록합니다.
- 문서를 다시 쓸 때는 기존 노트를 `notion-archive/`로 옮기고 현재판을 새로 만듭니다.

## 검증 문서 규칙

- 대표 검증 명령 1개와 demo/replay 명령 1개를 프로젝트 README와 `problem/README.md`에 모두 남깁니다.
- 테스트가 보장하는 사실과 아직 문서 수준인 가정은 분리해서 씁니다.
- reference vector나 fixture의 출처는 `problem/README.md`와 `docs/references/README.md`에 남깁니다.

