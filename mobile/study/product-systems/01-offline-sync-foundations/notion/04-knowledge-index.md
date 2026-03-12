# Knowledge Index — Offline Sync Foundations

## 연결된 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| `realtime-chat` | 후행 과제. 여기서 만든 queue/idempotency 패턴 위에 채팅 도메인을 얹는다. |
| `app-distribution` | 간접 연결. realtime-chat 앱의 스냅샷 기반이므로, 이 프로젝트의 sync 코드가 배포 대상에 포함된다. |
| `incident-ops-mobile-client` | 이 프로젝트의 최종 적용지. persistent outbox, retry count UI, DLQ 수동 재시도를 제품에 구현한다. |

## 재사용 가능한 패턴

### Outbox Queue 패턴
모든 mutation을 즉시 실행하지 않고 queue에 넣고, 연결 상태가 확인되면 flush하는 패턴.
채팅 메시지 전송, 인시던트 액션, 폼 제출 등 모든 오프라인 가능 mutation에 적용 가능하다.

### DLQ as State 패턴
영구 실패 job을 별도 컬렉션으로 옮기지 않고, 같은 큐 안에서 `state: 'dlq'`로 표현.
전체 큐를 한 번에 조회하면서 상태별 필터링만으로 관리할 수 있다.

### Deterministic Idempotency Key 패턴
`create-${localId}` 형태로 action + localId를 조합해 키를 만들면,
같은 리소스에 대한 중복 요청을 클라이언트-서버 양쪽에서 자연스럽게 감지할 수 있다.

### Pure Function Flush 패턴
`flushQueue(tasks, jobs, server)` → `{ tasks, jobs }` 형태로,
입력과 출력이 명확한 순수 함수로 동기화 로직을 표현하면 before/after 비교 테스트가 쉬워진다.

## 핵심 파일 참조

| 파일 | 역할 |
|------|------|
| `react-native/src/syncEngine.ts` | 전체 동기화 엔진 (TaskRecord, QueueJob, FakeSyncServer, flushQueue) |
| `react-native/src/OfflineSyncStudyApp.tsx` | 큐 상태 요약을 보여주는 앱 shell |
| `react-native/tests/offline-sync.test.ts` | sync, DLQ, idempotency, merge 테스트 |
| `docs/concepts/queue-replay-model.md` | 공개 문서용 큐 모델 설명 |

## 이 프로젝트에서 사용한 도구와 버전

- React Native 0.84.1
- AsyncStorage ^3.0.1
- NetInfo ^12.0.1
- TypeScript ^5.8.3
- Jest ^29.6.3
