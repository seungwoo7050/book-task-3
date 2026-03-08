# Chat Bot Challenge Study Repository

이 레포는 채용 연계 프로젝트 설명회에서 제시된 3개 과제를 `study1/`, `study2/`, `study3/`로 다시 설계한 저장소다.
모든 트랙은 “공고 기반 요구를 충족하는 경쟁력 있는 제출물”을 목표로 하며, `00~07` 미니과제가 `08-capstone-submission`을 직접 쌓아 올리도록 고정한다.

## Structure

```text
chat-bot/
├── docs/      # 세 과제 공통 해석, 선택 근거, 커리큘럼, 레퍼런스
├── legacy/    # 원본 자료 + 이전 시도 + 과거 구현
├── study1/    # MCP 추천 최적화
├── study2/    # 챗봇 상담 품질 관리
└── study3/    # 음성 회의 어시스턴트
```

## Track Overview

- `study1/`
  - 운영형 MCP 추천 시스템을 목표로 한다.
  - TypeScript/Node 중심으로 registry, recommendation, release gate를 누적한다.
- `study2/`
  - 상담 품질 QA Ops 플랫폼을 목표로 한다.
  - Python/React 중심으로 quality rubric, evaluation pipeline, dashboard를 누적한다.
- `study3/`
  - 한국어 회의 지원 시스템을 목표로 한다.
  - TypeScript realtime stack과 한국어 STT/meeting support 파이프라인을 누적한다.

## Version Policy

모든 `studyN/08-capstone-submission/`은 아래를 따른다.

1. `v0-*`: 최초 제출 가능한 데모
2. `v1-*`: `v0` 폴더 복제 후 경쟁력 핵심 강화
3. `v2-*`: `v1` 폴더 복제 후 제출 마감본
4. 필요 시 `v3-*`: `v2`를 self-hosted OSS 또는 운영형 snapshot으로 승격한 후속 버전

버전 폴더는 덮어쓰지 않는다.

현재 `study2/08-capstone-submission/v3-self-hosted-oss`가 self-hosted reference OSS target이고, `study2`의 `v0~v2`는 archive/demo 역할을 유지한다.

## How To Read

1. `docs/legacy-intent-audit.md`
2. `docs/project-selection-rationale.md`
3. `docs/curriculum-map.md`
4. 각 `studyN/README.md`
5. 각 `studyN/08-capstone-submission/README.md`
