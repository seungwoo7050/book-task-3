# Verification Policy

이 저장소의 검증은 "실제로 다시 설치하고, 실행하고, 통과하는가"를 기준으로 한다.

## 기본 환경

- 패키지 매니저: `npm`
- Node 기준 버전: 20 LTS
- 활성 검증 경로: `study/`
- 레거시 자산: 참조 전용, 검증 기록은 새로 만든다

## 상태 판정 기준

- `planned`: 구조와 문제 경계만 고정되어 있고 구현/검증이 아직 없다
- `in-progress`: 구현 또는 이관 중이며 검증이 끝나지 않았다
- `verified`: fresh install 기준 install, test, typecheck 등 약속한 검증을 통과했다
- `archived`: 더 이상 활성 코스는 아니지만 참고 가치가 남아 있다

## 루트 검증 스크립트

`study/package.json`은 아래 검증 스크립트를 제공한다.

- `verify:foundations`
- `verify:internals`
- `verify:portfolio`
- `verify:core`

원칙은 아래와 같다.

- `verify:foundations`: 현재 `verified` 상태인 foundations 프로젝트만 실행
- `verify:internals`: 현재 `verified` 상태인 internals 프로젝트만 실행
- `verify:portfolio`: 현재 `verified` 상태인 portfolio 프로젝트만 실행
- `verify:core`: 위 세 스크립트를 커리큘럼 순서대로 묶는다

즉, 아직 `planned` 상태인 프로젝트가 있다고 해서 `verify:core`가 실패하면 안 된다.

## 현재 verified 범위

2026-03-08 기준 verified 상태인 핵심 프로젝트는 아래 둘이다.

- `react-internals/01-vdom-foundations`
- `frontend-portfolio/01-ops-triage-console`

`frontend-foundations`는 아직 구조만 잡힌 상태이므로 `verify:foundations`는 정보 메시지를 출력하고 성공 종료한다.

## 트랙별 기본 검증 기대치

- `frontend-foundations`: a11y smoke, DOM behavior, browser-state scenario, E2E smoke
- `react-internals`: typecheck, unit test, integration scenario, runtime limitation note
- `frontend-portfolio`: typecheck, unit/integration, E2E, 발표용 문서와 데모 동선

## 문서 작성 원칙

- 과거 실행 기록은 참고일 뿐, 현재 검증 상태로 쓰지 않는다.
- 검증 날짜와 범위는 새 워크스페이스 기준으로 다시 적는다.
- 명령은 실제 파일 경로와 스크립트에 근거해야 한다.
