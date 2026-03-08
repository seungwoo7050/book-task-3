# Legacy Audit

## legacy가 원래 가르치려던 것

`legacy/`는 Express와 NestJS를 병행 비교하면서 백엔드 아키텍처를 단계적으로 학습하는 트랙이었다.
핵심 주제는 다음 여섯 가지였다.

1. REST API
2. Auth guards
3. Pipeline
4. Database
5. Event system
6. Platform capstone

## 재사용한 자산

- 챕터별 `problem/README.md`, `problem/code/`, `problem/Makefile`
- `solve/solution/` 아래의 실제 구현 코드와 테스트
- `docs/` 아래의 개념 문서
- 챕터 README와 lab report에서 드러난 목표와 비교 축

## study로 그대로 가져오지 않은 것

- `node_modules`
- `.vite`, 테스트 결과 JSON, 임시 로그
- raw `devlog/` 복사본
- 검증 재실행 없이 적힌 성공 주장

## 확인한 주요 이슈

- legacy는 문서상 재현성을 강조하지만, 현재 체크아웃 상태에서 `01-rest-api` 테스트는 바로 통과하지 않았다.
- 원인은 `vitest` 의존성이 설치되지 않은 상태여서 `node_modules/vitest/vitest.mjs`를 찾지 못한 것이다.
- 따라서 `study/`에서는 실제로 재실행한 명령만 `verified`로 표시한다.

## 재설계 결정

- `pipeline`을 `auth`보다 먼저 배치했다.
- 초보 브리지로 `00`, `01`, `02`를 추가했다.
- 운영/배포/관측성 브리지로 `08-production-readiness`를 추가했다.
- `legacy/`는 보존하되, 학습 진입점으로는 더 이상 사용하지 않는다.

