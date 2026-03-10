# 04 — Knowledge Index: Incident Ops Mobile Client 기술 색인

## 파일 맵

### src/lib/ — 인프라 계층

| 파일 | 역할 | 핵심 export |
|------|------|-------------|
| api.ts | HTTP/WS 통신 | loginRequest, listIncidents, listAudit, create/ack/requestResolution/decideApproval + ApiError, normalizeBaseUrl, buildWebsocketUrl |
| storage.ts | AsyncStorage 추상화 | loadSession/saveSession, loadSettings/saveSettings, loadOutbox/saveOutbox, loadLastEventId/saveLastEventId, createMemoryStorage |
| outbox.ts | 오프라인 큐 로직 | createQueuedMutation, markQueuedMutationSynced/Failed, retryQueuedMutation, summarizeOutbox, buildIncidentList |
| stream.ts | WebSocket 래퍼 | openIncidentStream |
| connectivity.ts | NetInfo 래퍼 | toConnectionState, fetchCurrentConnection, subscribeToConnectivity |
| forms.ts | Zod 스키마 | loginSchema, createIncidentSchema, resolutionSchema, approvalDecisionSchema |
| queries.ts | React Query 키 | incidentKeys, auditKeys |
| types.ts | 앱 로컬 타입 | AppSettings, AppSession, ConnectionState, StreamStatus, QueuedMutation, IncidentListItem |

### src/app/ — 상태 관리

| 파일 | 역할 |
|------|------|
| AppModel.tsx | Context Provider + useAppModel + useIncidentItems + usePendingApprovalItems + useIncidentAudit |

### src/screens/ — 화면

| 파일 | 화면 | 핵심 기능 |
|------|------|-----------|
| LoginScreen.tsx | 로그인 | react-hook-form + zod, 역할 선택 |
| LoadingScreen.tsx | 부트스트랩 | AsyncStorage 복원 중 표시 |
| IncidentsScreen.tsx | 인시던트 목록 | FlatList, 커서 페이지네이션, outbox summary |
| CreateIncidentScreen.tsx | 인시던트 생성 | zod 폼 검증, outbox enqueue |
| IncidentDetailScreen.tsx | 상세 + 액션 | canAck/canRequestResolution/canDecide, audit timeline |
| ApprovalsScreen.tsx | 승인 대기열 | RESOLUTION_PENDING 필터 |
| OutboxScreen.tsx | 오프라인 큐 | pending/synced/failed, retry, flush |
| SettingsScreen.tsx | 설정 | base URL 변경, 로그아웃, 메트릭 |

### src/navigation/

| 파일 | 역할 |
|------|------|
| RootNavigator.tsx | AuthStack / MainTabs 분기 |
| types.ts | AuthStackParamList, IncidentStackParamList, MainTabParamList |

### src/components/

| 파일 | 역할 |
|------|------|
| Ui.tsx | ScreenLayout, SectionCard, ActionButton, AppTextField, StatusPill, MetricRow, EmptyState |

## 네비게이션 구조

```
RootNavigator
├── LoadingScreen (bootstrapState !== 'ready')
├── AuthStack (session === null)
│   └── Login
└── MainTabs — Bottom Tabs (session exists)
    ├── IncidentsTab — Native Stack
    │   ├── IncidentFeed
    │   ├── CreateIncident
    │   └── IncidentDetail
    ├── Approvals
    ├── Outbox
    └── Settings
```

## 타입 시스템

### 앱 로컬 타입 (contracts에 없는 것)

| 타입 | 위치 | 용도 |
|------|------|------|
| AppSettings | types.ts | baseUrl |
| AppSession | types.ts | token + AuthActor |
| ConnectionState | types.ts | isConnected, typeLabel, updatedAt |
| StreamStatus | types.ts | 'idle' \| 'connecting' \| 'live' \| 'error' |
| QueuedMutation | types.ts | QueueJob + label + createdAt |
| IncidentListItem | types.ts | Incident + source + syncState + pendingActions |
| LoginFormValues | forms.ts | zod infer |
| CreateIncidentFormValues | forms.ts | zod infer |

### QueueAction (contracts)

```
'POST /incidents'
'POST /incidents/:id/ack'
'POST /incidents/:id/request-resolution'
'POST /approvals/:id/decision'
```

## Outbox 상태 머신

```
pending ──(flush 성공)──▶ synced
pending ──(flush 실패, attempts < 3)──▶ pending (attempts++)
pending ──(flush 실패, attempts >= 3)──▶ failed
failed ──(수동 retry)──▶ pending (attempts 유지, lastError null)
```

## API 엔드포인트

| 메서드 | 경로 | 용도 |
|--------|------|------|
| POST | /auth/login | 로그인 |
| GET | /incidents?limit=&cursor= | 인시던트 목록 (페이지네이션) |
| POST | /incidents | 인시던트 생성 |
| POST | /incidents/:id/ack | 인시던트 확인 |
| POST | /incidents/:id/request-resolution | 해결 요청 |
| POST | /approvals/:id/decision | 승인/거절 |
| GET | /audit?incidentId= | 감사 로그 |
| WS | /ws?lastEventId= | 실시간 이벤트 스트림 |

## Makefile 타겟

| 타겟 | 명령 | 용도 |
|------|------|------|
| test | verify | 기본 검증 |
| app-build | npm run typecheck | 타입 체크 |
| app-test | npm test | Jest 테스트 |
| server-test | cd node-server && npm test | 서버 테스트 |
| demo-e2e | node-server demo-e2e + maestro (optional) | e2e 데모 |

## 의존성

### 런타임

| 패키지 | 버전 | 용도 |
|--------|------|------|
| react-native | 0.84.1 | 프레임워크 |
| react | 19.2.3 | UI 라이브러리 |
| react-hook-form | ^7.71.2 | 폼 상태 관리 |
| @hookform/resolvers | ^5.2.2 | zod 연동 |
| zod | ^4.3.6 | 스키마 검증 |
| @tanstack/react-query | ^5.90.21 | 서버 상태 캐시 |
| @react-native-async-storage/async-storage | ^3.0.1 | 영속화 |
| @react-native-community/netinfo | ^12.0.1 | 네트워크 상태 |
| @react-navigation/native | ^7.1.33 | 네비게이션 코어 |
| @react-navigation/bottom-tabs | ^7.15.5 | 탭 네비게이션 |
| @react-navigation/native-stack | ^7.14.4 | 스택 네비게이션 |
| react-native-gesture-handler | ^2.30.0 | 제스처 |
| react-native-safe-area-context | ^5.5.2 | Safe Area |
| react-native-screens | ^4.24.0 | 네이티브 스크린 |
| @incident-ops/contracts | file:../problem/code/contracts | 공유 계약 |

### 개발

| 패키지 | 버전 | 용도 |
|--------|------|------|
| typescript | ^5.8.3 | 타입 시스템 |
| jest | ^29.6.3 | 테스트 러너 |
| @testing-library/react-native | ^13.3.3 | UI 테스트 |

## 연관 프로젝트

| 프로젝트 | 관계 | 공유 기술 |
|----------|------|-----------|
| incident-ops-mobile (harness) | 계약 + 워크플로우 모델 원본 | @incident-ops/contracts |
| realtime-chat | WebSocket 패턴 선행 학습 | StreamEvent 기반 실시간 |
| offline-sync-foundations | AsyncStorage 큐 선행 학습 | QueueJob, outbox 패턴 |
| navigation | @react-navigation v7 선행 학습 | Stack + Tab 네비게이션 |
| app-distribution | 배포 파이프라인 참고 | Fastlane, CodePush |

## 데모 아티팩트

| 파일 | 위치 | 내용 |
|------|------|------|
| audit-log.json | demo/ | 감사 로그 샘플 |
| e2e-summary.json | demo/ | e2e 테스트 결과 |
| structured-logs.json | demo/ | 서버 구조화 로그 |
| portfolio-presentation.md | docs/ | 13슬라이드 발표 스크립트 |
| 01-portfolio-core.yaml | react-native/maestro/ | 핵심 플로우 e2e |
| 02-portfolio-outbox-recovery.yaml | react-native/maestro/ | 장애 복구 e2e |
