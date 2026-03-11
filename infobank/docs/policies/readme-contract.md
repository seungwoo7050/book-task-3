# README Contract

이 레포의 README는 GitHub front door 문서다. 길게 설명하기보다 먼저 `문제가 무엇인가`, `이 레포의 공식 답이 어디인가`, `어떻게 검증하는가`, `더 긴 문서는 어디에 있는가`를 바로 찾게 해야 한다.

## 루트 README

- 두 과제의 `문제 / 공식 답(v2) / 확장 답(v3) / canonical verify / 시작 위치` 표를 먼저 보여 준다.
- `projects/`, `docs/`, `.github/` 구조를 짧게 설명한다.
- 공용 문서와 문서 정책 링크를 제공한다.

## 프로젝트 README

- 순서를 `문제 / 공식 답 / 확장 답 / 검증 / 읽는 순서 / 현재 한계`로 고정한다.
- 공식 답은 `capstone/v2-submission-polish`, 확장 답은 `capstone/v3-*`를 전면에 둔다.
- `problem/README.md`, `docs/README.md`, `capstone/README.md`, `docs/verification-matrix.md`를 엔트리포인트로 연결한다.

## Stage README

- 반드시 아래 6문답을 같은 순서로 답한다.
- `이 stage의 문제`
- `입력/제약`
- `이 stage의 답`
- `capstone 연결 증거`
- `검증 명령`
- `현재 한계`

## Capstone README

- 버전 표로 `v0 baseline`, `v1 hardening`, `v2 official answer`, `v3 extension`을 구분한다.
- 공식 제출 답과 확장 버전을 동시에 설명하되, 우선순위는 `v2 -> v3 -> v1 -> v0` 순으로 둔다.

## 하위 README

- `problem/README.md`: 문제 해석, 제공 자료, 범위, 완료 기준
- `docs/README.md`: 해당 계층의 durable notes index
- `notion/README.md`: 읽기 순서와 문서 역할만 안내
- `notion-archive/README.md`: pre-migration 기록임을 먼저 알린다

## 언어 정책

- 설명 문장과 authored code comment/docstring은 한국어를 기본으로 쓴다.
- 식별자, 파일 경로, 명령, 라이브러리명, 프로토콜명, env var, literal output은 영어 원문을 유지한다.
