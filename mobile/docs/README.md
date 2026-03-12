# Repository Docs

루트 `docs/`는 저장소 전체에 적용되는 커리큘럼 설명과 검증 기준만 담는다.
프로젝트별 구현 세부나 디버깅 로그는 각 프로젝트 `docs/`와 `notion/` 아래로 내린다.

## 문서 목록

- [curriculum-map.md](curriculum-map.md): `study/` stage 구조와 읽는 순서
- [junior-end-skill-bar.md](junior-end-skill-bar.md): 이 저장소가 증명하려는 RN 역량 기준
- [repo-improvement-roadmap.md](repo-improvement-roadmap.md): 저장소 개선 맥락과 남은 정리 포인트
- [legacy-audit.md](legacy-audit.md): 과거 구조의 흔적과 왜 현재 구조로 재편했는지
- [path-migration-map.md](path-migration-map.md): old path -> new path 이행표

## 문서 역할

- 루트 README: 저장소 landing page
- `study/README.md`: 전체 curriculum index
- stage README: 단계 목적과 포함 프로젝트
- 프로젝트 README: 문제와 답
- 프로젝트 `docs/README.md`: 안정적인 개념 문서 인덱스
- 프로젝트 `notion/README.md`: 장기 보관 학습 로그 인덱스

## 검증

```bash
bash ../scripts/check_study_docs.sh
bash ../scripts/verify_study_structure.sh
bash ../scripts/report_study_status.sh
```
