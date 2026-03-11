> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../docs/catalog/path-migration-map.md)를 본다.

# Stage 08 — Capstone Submission 노트 가이드

이 폴더는 mcp-recommendation-demo의 마지막 stage인 **Capstone Submission**의 설계 과정을 담고 있다.  
v0 → v1 → v2 → v3로 이어지는 전체 시스템의 반복적 확장 과정을 기록한다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 왜 4단계 반복인지, 각 버전의 범위 정의 |
| 2 | [01-approach-log.md](./01-approach-log.md) | v0→v1→v2→v3 구현 전략과 기술 선택 |
| 3 | [02-debug-log.md](./02-debug-log.md) | DB 마이그레이션, auth 세션, Docker 빌드 등 문제 |
| 4 | [03-retrospective.md](./03-retrospective.md) | 4단계 반복의 효과와 한계 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | 전체 스택 구성, v0-v3 비교표, 핵심 API |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | 전체 빌드·실행·테스트·배포 명령어 |

## 관련 stage

- **이전**: [07-operator-dashboard](../../07-operator-dashboard-and-experiment-console/notion/) — 대시보드 설계
- **전체 curriculum**: 모든 stage(00-07)의 문제 정의와 설계가 이 capstone에서 실제 코드로 구현됨
