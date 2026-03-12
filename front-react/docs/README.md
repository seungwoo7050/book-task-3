# 저장소 공통 문서

이 디렉터리는 `front-react` 전체에 적용되는 규칙, 커리큘럼, 검증 기준을 모은다. 루트 README가 "무슨 프로젝트가 있는가"를 설명한다면, 이 디렉터리는 "이 저장소를 어떤 규칙으로 읽고 유지하는가"를 설명한다.

## 먼저 읽을 문서

- [project-template.md](project-template.md): 프로젝트 README, `problem/README`, 구현 디렉터리, `docs/`, `notion/`의 역할 계약
- [verification-policy.md](verification-policy.md): `verified` 판정 기준과 워크스페이스 검증 명령
- [curriculum-map.md](curriculum-map.md): 3트랙 9프로젝트의 순서와 핵심 질문

## 문서 목록

- [curriculum-map.md](curriculum-map.md): 전체 핵심 경로와 읽는 순서
- [junior-skill-matrix.md](junior-skill-matrix.md): 주니어 끝자락 기준 역량과 프로젝트 매핑
- [legacy-audit.md](legacy-audit.md): 기존 internals 자산을 어떻게 새 경로로 압축했는지에 대한 근거
- [notion-readiness-audit.md](notion-readiness-audit.md): `notion/` 문서 품질과 공개 공유 가능 여부 점검 기준
- [verification-policy.md](verification-policy.md): 설치, 테스트, 타입체크, 상태 판정 기준
- [project-template.md](project-template.md): 프로젝트 구조와 문서 계약의 소스 오브 트루스

## 사용 원칙

- 저장소 설명은 현재 실제 경로와 실제 명령을 기준으로 쓴다.
- public README는 answer dump가 아니라 빠른 인덱스와 재현 절차를 제공해야 한다.
- `problem/README.md`는 문제와 제약을 설명하고, 프로젝트 README는 답과 검증을 요약해야 한다.
- `docs/`와 README만 읽어도 프로젝트를 이해할 수 있어야 하며, `notion/`은 보조 학습 노트로만 읽힌다.
