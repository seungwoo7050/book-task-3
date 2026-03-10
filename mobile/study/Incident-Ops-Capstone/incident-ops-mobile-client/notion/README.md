# Incident Ops Mobile Client — Notion 문서 가이드

## 이 폴더의 목적

incident-ops-mobile-client는 이 학습 저장소의 최종 캡스톤 프로젝트다.
harness에서 검증한 인시던트 워크플로우를 실제 React Native 완성작으로 구현한다.
8개 화면, persistent outbox, WebSocket replay, react-hook-form + zod 검증,
@tanstack/react-query 캐시, AsyncStorage 영속화, Maestro e2e — 모든 것이 하나의 앱에 들어있다.

## 문서 읽기 순서

### 처음 이 프로젝트를 접하는 경우

1. [00-problem-framing.md](./00-problem-framing.md) — 왜 이 앱을 만들었는가, MVP 범위, 아키텍처 전체 그림
2. [01-approach-log.md](./01-approach-log.md) — 계층별 구현 과정 (lib → AppModel → screens → navigation)
3. [03-retrospective.md](./03-retrospective.md) — 설계 판단의 근거와 결과

### 특정 문제를 추적하는 경우

- [02-debug-log.md](./02-debug-log.md) — outbox 상태 전이, WebSocket 재연결, optimistic UI 관련 이슈

### 파일 구조나 API를 빠르게 참조하는 경우

- [04-knowledge-index.md](./04-knowledge-index.md) — 파일 맵, 의존성, 타입, 화면 목록, 네비게이션 구조

### CLI 명령어나 도구 사용 이력을 확인하는 경우

- [05-development-timeline.md](./05-development-timeline.md) — npm install, 서버 실행, Maestro 설정, 시뮬레이터 캡처 과정

## 연관 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| incident-ops-mobile(harness) | 이 클라이언트의 설계 청사진. contract + 워크플로우 모델 |
| realtime-chat | WebSocket 실시간 통신 패턴의 선행 학습 |
| offline-sync-foundations | AsyncStorage 오프라인 큐 패턴의 선행 학습 |
| app-distribution | Fastlane + CodePush 배포 파이프라인 (이 앱의 배포 시 참고) |
| navigation | @react-navigation v7 라우팅 패턴의 선행 학습 |
