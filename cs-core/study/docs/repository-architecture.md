# repository-architecture

이 문서는 `cs-core/study`의 공개 표면과 내부 학습 레이어를 어떻게 나누는지 고정한다.

## 기본 레이어

- 루트 `README.md`: 4개 트랙과 15개 프로젝트를 빠르게 탐색하는 대시보드
- 트랙 `README.md`: 같은 주제의 프로젝트를 묶어 읽는 지도
- 프로젝트 `README.md`: `문제`, `답`, `검증`, `공개 경계`를 한 화면에 보여 주는 진입점

## 디렉터리 책임

| 경로 | 책임 | 공개 원칙 |
| --- | --- | --- |
| `problem/` | 문제 계약, starter boundary, 공식 검증 경계, local-only 자산 안내 | 원문 계약과 검증 절차를 보존한다. 공식 자산은 source tone을 유지할 수 있다. |
| `c/`, `cpp/`, `python/`, `y86/`, `src/` | 내가 작성한 실행 가능한 답 | authored comment는 한국어를 기본으로 한다. |
| 프로젝트 `docs/` | 개념 설명, 검증 해설, durable note | README보다 길어도 되지만 답안 덤프처럼 쓰지 않는다. |
| 프로젝트 `notion/` | 현재판 접근 로그, 디버그 근거, 재현 타임라인 | 장문 reasoning과 rebuild log를 둔다. |
| 프로젝트 `notion-archive/` | 이전 버전 노트, 폐기된 시도, superseded draft | 현재판에서 밀려난 내용을 보존한다. |
| 루트 `docs/` | 저장소 공통 규칙, 커리큘럼 맵, 상태 표 | 프로젝트별 세부 reasoning은 넣지 않는다. |
| 루트 `scripts/` | local-only asset 복원, 공식 검증 보조 스크립트 | 공개 표면 설명 대신 실행 보조 역할만 맡는다. |

## 언어 규칙

- 설명용 prose와 authored code comment는 한국어를 기본으로 쓴다.
- 명령어, 파일 경로, tool name, protocol name, code identifier, 원문 과제 이름은 English 그대로 둔다.
- `problem/` 아래 공식 자산과 starter 텍스트는 원문 계약 보존이 우선이다.

## 이동하지 않는 것

- 트랙 루트 4개와 프로젝트 루트 15개는 유지한다.
- 구현 디렉터리 이름(`c/`, `cpp/`, `python/`, `y86/`, `src/`)과 canonical verification path는 유지한다.
- `notion/`과 `notion-archive/`의 이중 구조는 이미 존재하는 프로젝트에서 그대로 보존한다.
