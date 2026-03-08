# Repository Docs

루트 문서는 레거시 해석, 새 커리큘럼, 마이그레이션 정책을 저장소 수준에서 설명한다.

## Documents

- [curriculum-map.md](curriculum-map.md): `study/` 트랙 구성과 학습 순서
- [junior-end-skill-bar.md](junior-end-skill-bar.md): 이 저장소가 증명해야 하는 RN 역량 기준
- [repo-improvement-roadmap.md](repo-improvement-roadmap.md): 저장소를 실제 학습 경로로 완성하기 위한 우선순위
- [legacy-audit.md](legacy-audit.md): `legacy/` 상태 감사와 설계 결함

## Verification

```bash
bash ../scripts/report_study_status.sh
bash ../scripts/check_study_docs.sh
bash ../scripts/verify_study_structure.sh
```

## Policy

- 루트 문서는 `legacy/` 대신 `study/`를 기준으로 링크를 건다.
- 구현 상태 표기는 `planned`, `in-progress`, `verified`, `archived`만 사용한다.
- 추정이나 미검증 주장은 `legacy-audit.md`에 한정하고, `study/` 문서에는 재현 가능한 명령을 우선 기록한다.
- 루트 문서는 현재 검증된 역량과 아직 비어 있는 역량을 둘 다 드러내야 한다.
