# Curriculum Map

이 저장소의 목표는 React Native 제품 개발 역량을 과제 단위로 학습하는 것이다.
`legacy/`는 문제군의 흔적을 보여 주지만, `study/`는 실제 학습 순서와 프로젝트 경계를 다시 정한 결과물이다.

## Track Order

### 1. Mobile-Foundations

1. `navigation`
2. `virtualized-list`
3. `gestures`

핵심 주제:
- 화면 구조와 navigation state
- 대형 리스트 렌더링과 성능 계측
- Gesture Handler, Reanimated 기반 상호작용

### 2. React-Native-Architecture

1. `bridge-vs-jsi`
2. `native-modules`

핵심 주제:
- New Architecture 개념
- Bridge와 JSI의 비용 차이
- Swift/Kotlin 네이티브 모듈 설계

### 3. Chat-Product-Systems

1. `offline-sync-foundations`
2. `realtime-chat`
3. `app-distribution`

핵심 주제:
- 오프라인 큐, 동기화, 충돌 해결
- WebSocket과 로컬 데이터 계층 통합
- 배포 자동화와 OTA 업데이트

`offline-sync-foundations`는 새로 추가한 브리지 프로젝트다.
기존 레거시 셋은 UI/아키텍처에서 곧바로 WatermelonDB 기반 실시간 채팅으로 넘어가 학습 간격이 컸다.

### 4. Incident-Ops-Capstone

1. `incident-ops-mobile`
2. `incident-ops-mobile-client`

핵심 주제:
- 모바일 클라이언트와 Node 백엔드 계약
- 승인 플로우와 감사 로그
- 오프라인 복구와 데모 재현성
- 채용 제출용 RN 제품 완성도

## Why This Shape

- 기초 UI 과제는 React Native 화면 모델과 성능 특성을 먼저 고정한다.
- 아키텍처 트랙은 네이티브 연동과 RN 런타임 구조를 이해하게 만든다.
- 채팅/제품화 트랙은 오프라인 우선 제품 설계를 단계적으로 쌓게 만든다.
- 첫 capstone은 시스템/계약 경계를 고정하고, 마지막 capstone은 같은 도메인을 RN 완성작으로 다시 구현한다.

## Validation Rule

각 프로젝트는 다음 네 가지를 분명히 보여야 한다.

1. 문제 원문 또는 재정의된 문제 범위
2. 실행 가능한 구현 경로
3. 재현 가능한 검증 명령
4. 학습 포인트와 현재 상태
