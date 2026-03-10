# Development Timeline — Offline Sync Foundations

이 문서는 프로젝트의 전체 개발 과정을 시간순으로 기록한다.
소스코드만으로는 알 수 없는 CLI 명령, 설치 과정, 설정 변경, 의사결정 맥락을 포함한다.

---

## Phase 1: 프로젝트 초기화

### React Native 프로젝트 생성

```bash
npx @react-native-community/cli init OfflineSyncFoundationsStudy --version 0.84.1
cd OfflineSyncFoundationsStudy
```

이 프로젝트는 레거시 소스에서 마이그레이션한 것이 아니라, 학습 목적으로 새로 설계한 프로젝트다. `realtime-chat`의 선행 과제로서 동기화 기초만 격리해서 다룬다.

### 핵심 의존성 설치

```bash
npm install @react-native-async-storage/async-storage@^3.0.1
npm install @react-native-community/netinfo@^12.0.1
npm install @testing-library/react-native@^13.3.3
```

AsyncStorage는 큐 영속화 실험용, NetInfo는 네트워크 상태 감지용으로 설치했다. 이 프로젝트에서는 두 라이브러리 모두 앱 shell에서만 참조하고, 핵심 로직 테스트에는 사용하지 않는다.

### iOS 네이티브 의존성 연결

```bash
cd ios && bundle install && bundle exec pod install && cd ..
```

---

## Phase 2: 동기화 엔진 구현

### 타입 정의

`src/syncEngine.ts`에서 가장 먼저 네 가지 타입을 정의했다:

1. `QueueState` — `'pending' | 'synced' | 'failed' | 'dlq'` 유니언
2. `TaskRecord` — 로컬에서 생성한 태스크 레코드 (`localId`, `serverId`, `title`, `status`, `updatedAt`)
3. `QueueJob` — 큐에 들어가는 작업 단위 (`id`, `action`, `taskLocalId`, `payload`, `idempotencyKey`, `attempts`, `state`, `lastError`)

### createTaskDraft 함수

sequence 번호를 받아서 TaskRecord와 QueueJob을 동시에 생성하는 함수를 만들었다. idempotency key는 `create-local-${sequence}` 형태로 결정론적으로 생성된다.

### FakeSyncServer 클래스

인메모리 서버 시뮬레이터를 구현했다. 핵심 로직:
- `seenKeys` Map으로 이미 처리한 idempotency key를 추적
- payload에 `FAIL` 문자열이 포함되면 무조건 예외 발생 (테스트용 실패 트리거)
- 중복 키면 기존 serverId를 반환하고 `accepted: false`

### mergeServerAssignedFields 함수

서버가 돌려준 `serverId`와 `updatedAt`을 로컬 레코드에 병합하되, `title` 같은 클라이언트 소유 필드는 건드리지 않는 규칙을 구현했다.

### flushQueue 함수

큐 전체를 순회하며 각 pending/failed job을 서버에 시도하고, 결과에 따라 상태를 갱신하는 핵심 함수를 작성했다.

작성 순서:
1. 입력 배열을 복사해서 원본 불변성 보장
2. 각 job을 순회하면서 `pending`이나 `failed`인 것만 처리
3. try: 서버 호출 성공 → task에 server 필드 병합, job을 `synced`로
4. catch: 실패 → `attempts` 증가, `maxAttempts` 초과 시 `dlq`로, 아니면 `failed`로

---

## Phase 3: 테스트 작성

### offline-sync.test.ts

네 가지 테스트를 작성했다:

```bash
npm test -- --verbose
```

1. **정상 동기화** — pending task가 flush 후 `serverId`를 받고 `synced`가 되는지
2. **DLQ 전환** — `FAIL` payload를 가진 job이 두 번 flush 후 `dlq`로 이동하는지
3. **Idempotency 안정성** — 같은 서버에 같은 키로 두 번 flush하면 같은 `serverId`를 받는지
4. **필드 병합** — `mergeServerAssignedFields`가 serverId를 채우면서 title은 보존하는지

DLQ 테스트에서는 의도적으로 두 개의 서로 다른 `FakeSyncServer` 인스턴스를 사용한다. 첫 번째 서버에서 실패하고, 두 번째 서버에서도 실패해야 DLQ로 이동하기 때문이다 (만약 같은 서버를 사용하면 idempotency key 때문에 두 번째 시도가 다르게 동작할 수 있다).

---

## Phase 4: 앱 Shell 구현

### OfflineSyncStudyApp.tsx

학습 데모용 UI를 만들었다. 실제 동기화 과정을 시각적으로 보여주기보다는, 큐 상태의 before/after를 화면에 요약하는 정도다.

구성:
1. 상단 프로젝트 제목과 설명
2. Queue Status 카드 — 각 job의 상태와 시도 횟수
3. Task Records 카드 — 로컬/서버 ID와 동기화 상태

---

## Phase 5: 빌드 검증

```bash
# TypeScript 타입 체크
npm run typecheck

# 전체 검증
npm run verify    # typecheck + test

# Make 기반 검증
cd problem
make test         # verify_task.sh → 필수 파일 점검
make app-build    # npm install + typecheck
make app-test     # npm install + jest
```

---

## Phase 6: 문서 정비

- `docs/concepts/README.md` — outbox, retry/DLQ, merge rule 핵심 원칙
- `docs/concepts/queue-replay-model.md` — 큐 flush 순서와 idempotency 규칙
- `docs/references/README.md` — 프로젝트 참조 경로

---

## 사용한 CLI 명령 전체 요약

| 단계 | 명령 | 목적 |
|------|------|------|
| 초기화 | `npx @react-native-community/cli init` | RN 프로젝트 생성 |
| 의존성 | `npm install @react-native-async-storage/async-storage ...` | 핵심 라이브러리 설치 |
| iOS | `cd ios && bundle install && bundle exec pod install` | 네이티브 의존성 연결 |
| 테스트 | `npm test` | Jest 실행 |
| 타입 | `npm run typecheck` | TypeScript 검증 |
| 검증 | `npm run verify` | typecheck + test |
| 빌드 | `make app-build` | Make 기반 빌드 |
