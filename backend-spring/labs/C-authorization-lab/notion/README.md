# C-authorization-lab Notion 문서 가이드

이 폴더는 C-authorization-lab(인가 — RBAC, membership, ownership)의 개발 과정과 학습 내용을 기록한 문서 세트다.

## 어떤 문서를 읽어야 하는가

### 처음 이 프로젝트를 접하는 경우
1. **[00-problem-framing.md](./00-problem-framing.md)** — 인증과 인가를 왜 분리했는지, 이 랩의 범위를 이해한다.
2. **[05-timeline.md](./05-timeline.md)** — 프로젝트를 처음부터 재현하고 싶다면 이 문서를 따라간다.
3. **[01-approach-log.md](./01-approach-log.md)** — service logic vs method security 결정의 근거.

### 특정 문제를 디버깅하는 경우
- **[02-debug-log.md](./02-debug-log.md)** — authorization 문서화의 과장 방지.

### 학습 내용을 복습하는 경우
- **[04-knowledge-index.md](./04-knowledge-index.md)** — RBAC, membership lifecycle, ownership check 개념 정리.
- **[03-retrospective.md](./03-retrospective.md)** — 강점, 약점, 다음 단계.

## 문서 목록

| 번호 | 파일 | 목적 |
|------|------|------|
| 00 | problem-framing | 인가 문제 정의와 성공 기준 |
| 01 | approach-log | service logic 중심 설계 결정 근거 |
| 02 | debug-log | 구현 깊이와 문서 설명의 간극 |
| 03 | retrospective | 회고 — invite lifecycle, ownership 학습 |
| 04 | knowledge-index | RBAC, method security 개념과 용어 |
| 05 | timeline | 전체 개발 과정의 순차적 기록 |
