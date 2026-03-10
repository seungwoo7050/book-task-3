# 00 — Problem Framing: Incident Ops Mobile Client

## 왜 이 프로젝트가 존재하는가

incident-ops-mobile(harness)은 "서버 없이 워크플로우를 검증"하는 프로젝트였다.
이 프로젝트는 그 검증된 워크플로우를 **실제 제품 수준의 React Native 앱**으로 구현한다.

핵심 질문은 하나다:
> "role-based workflow, persistent outbox, replay-safe realtime, shared contract를
> 하나의 모바일 제품 경험으로 묶을 수 있는가?"

이것이 채용 포트폴리오 캡스톤으로서의 이 앱의 존재 이유다.

## MVP 범위

problem/README.md가 정의한 7가지 필수 기능:

1. **Auth entry** — 역할 선택 + 세션 복원
2. **Incident feed** — 커서 페이지네이션 + 수동 새로고침
3. **Incident create form** — zod 검증
4. **Role-based actions** — OPERATOR: ack, request-resolution / APPROVER: approve, reject
5. **Audit timeline** — 인시던트 상세에서 감사 기록 표시
6. **Persistent outbox** — retry count, failed state, manual retry
7. **WebSocket reconnect replay** — lastEventId 기반

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────┐
│  @incident-ops/contracts (공유 계약)                  │
│  Incident, Approval, AuditLog, StreamEvent, QueueJob │
└──────────┬───────────────────────────────┬──────────┘
           │                               │
    ┌──────▼──────┐                 ┌──────▼──────┐
    │ node-server │                 │ react-native │
    │ (Express)   │◄────REST/WS───▶│ (RN 0.84.1)  │
    │ port: 4100  │                 │              │
    └─────────────┘                 └──────────────┘
```

### 클라이언트 내부 계층

```
contracts.ts (re-export)
    ↓
lib/ (api, storage, outbox, stream, connectivity, forms, queries, types)
    ↓
app/AppModel.tsx (Context + hooks, 전역 상태 관리)
    ↓
screens/ (8개 화면)
    ↓
navigation/RootNavigator.tsx (AuthStack / MainTabs)
    ↓
components/Ui.tsx (공유 UI 컴포넌트)
```

## 8개 화면

| 화면 | 역할 | 핵심 기능 |
|------|------|-----------|
| LoginScreen | 인증 진입점 | react-hook-form + zod, 역할 선택 버튼 |
| LoadingScreen | 부트스트랩 | AsyncStorage에서 세션/설정/outbox 복원 중 표시 |
| IncidentsScreen | 인시던트 목록 | FlatList + 커서 페이지네이션, outbox summary, stream status |
| CreateIncidentScreen | 인시던트 생성 | zod 폼 검증, outbox에 mutation 추가 |
| IncidentDetailScreen | 상세 + 액션 | 역할별 액션 버튼(ack/request-resolution/approve/reject), audit timeline |
| ApprovalsScreen | 승인 대기열 | RESOLUTION_PENDING 필터링 |
| OutboxScreen | 오프라인 큐 | pending/synced/failed 상태, retry, flush |
| SettingsScreen | 설정 | base URL 변경, 로그아웃, stream/connection 메트릭 |

## 네비게이션 구조

```
RootNavigator
├── bootstrapState !== 'ready' → LoadingScreen
├── session === null → AuthStack
│   └── Login
└── session exists → MainTabs (Bottom Tabs)
    ├── IncidentsTab (Stack)
    │   ├── IncidentFeed
    │   ├── CreateIncident
    │   └── IncidentDetail
    ├── Approvals
    ├── Outbox
    └── Settings
```

## 핵심 기술 스택

| 기술 | 용도 |
|------|------|
| react-hook-form + @hookform/resolvers | 폼 상태 관리 |
| zod v4 | 스키마 검증 |
| @tanstack/react-query v5 | 서버 상태 캐시, infinite query |
| AsyncStorage | 세션, 설정, outbox, lastEventId 영속화 |
| @react-native-community/netinfo | 네트워크 상태 감지 |
| WebSocket | 실시간 이벤트 스트림 |
| @react-navigation v7 | Bottom tabs + Native stack |
| Maestro | e2e 자동화 테스트 |

## 학습 경로에서의 위치

이 프로젝트는 전체 커리큘럼의 최종 도착점이다.

- **gestures, navigation, virtualized-list** → 모바일 기초
- **bridge-vs-jsi, native-modules** → RN 아키텍처 이해
- **realtime-chat** → WebSocket 패턴
- **offline-sync-foundations** → AsyncStorage 큐 패턴
- **app-distribution** → 빌드/배포 파이프라인
- **incident-ops-mobile (harness)** → 도메인 모델 검증
- **incident-ops-mobile-client** ← 모든 것의 종합
