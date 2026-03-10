# B-federation-security-lab Notion 문서 가이드

이 폴더는 B-federation-security-lab(인증 강화 — OAuth2 federation, 2FA, audit logging)의 개발 과정과 학습 내용을 기록한 문서 세트다.

## 어떤 문서를 읽어야 하는가

### 처음 이 프로젝트를 접하는 경우
1. **[00-problem-framing.md](./00-problem-framing.md)** — 왜 federation, 2FA, audit를 하나의 랩에 묶었는지 이해한다.
2. **[05-timeline.md](./05-timeline.md)** — 프로젝트를 처음부터 재현하고 싶다면 이 문서를 따라간다.
3. **[01-approach-log.md](./01-approach-log.md)** — 설계 결정의 이유가 궁금하면 이 문서를 본다.

### 특정 문제를 디버깅하는 경우
- **[02-debug-log.md](./02-debug-log.md)** — 보안 기능 문서화의 함정과 해결 과정.

### 학습 내용을 복습하는 경우
- **[04-knowledge-index.md](./04-knowledge-index.md)** — external identity linking, TOTP, audit log 개념 정리.
- **[03-retrospective.md](./03-retrospective.md)** — 무엇이 잘 됐고 무엇이 부족한지 돌아본다.

## 문서 목록

| 번호 | 파일 | 목적 |
|------|------|------|
| 00 | problem-framing | 이 랩이 풀려는 문제와 성공 기준 |
| 01 | approach-log | 설계 선택지와 최종 결정의 근거 |
| 02 | debug-log | 보안 문서화의 과장 방지 |
| 03 | retrospective | 완료 후 회고 — 강점, 약점, 다음 단계 |
| 04 | knowledge-index | 재사용 가능한 개념과 용어 정리 |
| 05 | timeline | 전체 개발 과정의 순차적 기록 (CLI, 설정, 구현) |
