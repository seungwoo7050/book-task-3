# React Native Study Archive

이 저장소는 React Native 학습 트리를 `legacy/`와 `study/`로 분리해 관리하는 학습 아카이브다.
`legacy/`는 읽기 전용 기준선이고, `study/`는 재구성된 학습 프로젝트와 실행 가능한 구현을 담는다.

## Repository Layout

- `legacy/`: 원본 레거시 트리. 링크 오류와 추정 문서를 포함한 기준선 보관용이다.
- `study/`: 새 학습 트리. 문제, 구현, 문서, 로컬 노트를 분리한다.
- `docs/`: 커리큘럼 해석, 레거시 감사, 저장소 공용 규칙.
- `scripts/`: `study/` 구조와 문서 링크 검증 스크립트.

## Study Tracks

- `study/Mobile-Foundations`
- `study/React-Native-Architecture`
- `study/Chat-Product-Systems`
- `study/Incident-Ops-Capstone`

캡스톤 트랙의 마지막 두 과제는 역할이 다르다.

1. `incident-ops-mobile`: 문제/계약/서버 중심 캡스톤
2. `incident-ops-mobile-client`: RN 채용 제출용 완성작

새 커리큘럼은 UI 기본기에서 아키텍처, 오프라인 동기화, 제품화, 캡스톤으로 이어지도록 재배열했다.
특히 `offline-sync-foundations`를 추가해 `realtime-chat` 진입 전 브리지 프로젝트를 만든다.

## Canonical Commands

```bash
bash scripts/bootstrap_study_tree.sh
bash scripts/report_study_status.sh
bash scripts/verify_study_structure.sh
bash scripts/check_study_docs.sh
```

`navigation` 파일럿 구현 검증:

```bash
cd study/Mobile-Foundations/navigation/react-native
npm install
npm run typecheck
npm test
npm run verify
```

## Current Status

- 저장소 인터페이스와 `study/` 골격: `verified`
- 학습 경로 10개 프로젝트: 모두 `verified`
- 두 캡스톤 역할 분리: `incident-ops-mobile`는 contract harness, `incident-ops-mobile-client`는 portfolio client
- 루트 검증 스크립트: `report_study_status`, `verify_study_structure`, `check_study_docs` 기준 유지 가능

## Repository Judgment

현재 저장소는 React Native 학습 커리큘럼의 방향뿐 아니라,
`초보자 -> 주니어 끝자락` 경로를 실제 프로젝트와 검증 명령으로 모두 채운 상태다.
기초 UI, 성능, interaction, 아키텍처 경계, 오프라인/실시간 제품 시스템, 배포 리허설,
계약 중심 캡스톤, 포트폴리오 클라이언트가 하나의 연속된 학습 경로로 정리돼 있다.

## Reading Order

1. `docs/README.md`
2. `docs/curriculum-map.md`
3. `docs/junior-end-skill-bar.md`
4. `docs/repo-improvement-roadmap.md`
5. `docs/legacy-audit.md`
6. `study/README.md`

## Notes

- `legacy/`는 수정하지 않는다.
- `study/**/notion/`은 로컬 전용이다.
- 문서 링크는 `study/`와 루트의 실제 파일만 기준으로 검증한다.
