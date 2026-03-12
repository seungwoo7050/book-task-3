# Development Timeline — Realtime Chat

이 문서는 프로젝트의 전체 개발 과정을 시간순으로 기록한다.
소스코드만으로는 알 수 없는 CLI 명령, 설치 과정, 설정 변경, 의사결정 맥락을 포함한다.

---

## Phase 1: 프로젝트 초기화

### React Native 프로젝트 생성

```bash
npx @react-native-community/cli init RealtimeChatStudy --version 0.84.1
cd RealtimeChatStudy
```

생성 후 `app.json`에서 앱 이름을 `RealtimeChatStudy`로 확인했다.
`tsconfig.json`은 `@react-native/typescript-config`를 extends하고, `jest` 타입과 `src/`, `tests/` 경로를 include에 추가했다.

### 핵심 의존성 설치

```bash
npm install @nozbe/watermelondb@^0.28.0
npm install @react-native-community/netinfo@^12.0.1
npm install @shopify/flash-list@^2.2.0
npm install @testing-library/react-native@^13.3.3
```

WatermelonDB는 로컬 영속성을 위해, NetInfo는 네트워크 상태 감지를 위해, FlashList는 메시지 목록 성능을 위해 선택했다. 시점에서 이 세 가지가 이 프로젝트의 핵심 외부 의존성이 됐다.

### iOS 네이티브 의존성 연결

```bash
cd ios && bundle install && bundle exec pod install && cd ..
```

WatermelonDB와 NetInfo 모두 네이티브 코드를 포함하므로 CocoaPods 설치가 필수였다. `Gemfile`에 Ruby 의존성이 이미 정의되어 있어 `bundle install`로 먼저 Bundler 환경을 맞췄다.

---

## Phase 2: 도메인 모델 구현

### chatModel.ts 작성

가장 먼저 `src/chatModel.ts`를 만들었다. 이 파일이 프로젝트의 핵심이다.

작성 순서:
1. `MessageRecord` 인터페이스 정의 — `clientId`, `serverId`, `conversationId`, `text`, `status`
2. `ReplayEvent` 인터페이스 정의 — `eventId`, `serverId`, `text`
3. `createPendingMessage()` — 새 메시지를 pending 상태로 생성
4. `reconcileAck()` — 서버 ack를 받아 pending → sent로 전환
5. `applyReplayEvents()` — `lastEventId` 이후 이벤트만 필터
6. `dedupeReplay()` — `serverId` 기준 중복 제거
7. `updateTypingState()` — typing 상태 업데이트 (인메모리)

각 함수를 순수 함수로 작성해서 외부 상태에 의존하지 않게 했다. 이 결정이 이후 테스트 작성을 매우 단순하게 만들었다.

### storageSchema.ts 작성

```typescript
// WatermelonDB appSchema로 messages 테이블 정의
// version: 1, 컬럼: server_id, client_id, conversation_id, text, status
```

`chatModel.ts`의 `MessageRecord`와 1:1 대응하되, WatermelonDB 컨벤션에 따라 snake_case 컬럼명을 사용했다. `server_id`는 `isOptional: true`로 설정해서 pending 메시지의 null 상태를 허용했다.

---

## Phase 3: 테스트 작성

### Jest 설정

`jest.config.js`에서 `preset: 'react-native'`를 사용하고, 테스트 파일 경로를 `tests/` 하위로 한정했다.

```bash
# jest.setup.ts 확인 후 테스트 실행
npm test
```

### realtime-chat.test.ts 작성

테스트 세 개를 작성했다:

1. **ack reconciliation 테스트** — pending 메시지에 ack를 적용하면 `serverId`가 채워지고 status가 `sent`로 바뀌는지
2. **replay 필터 테스트** — `lastEventId=1`이면 `eventId=2`인 이벤트만 남는지
3. **dedupe + typing 테스트** — 같은 `serverId`를 가진 이벤트가 하나로 줄어드는지, typing 상태가 정상 업데이트되는지

```bash
npm test -- --verbose
```

모든 테스트가 통과한 뒤에야 UI 작업으로 넘어갔다.

---

## Phase 4: UI Shell 구현

### RealtimeChatStudyApp.tsx 작성

앱 화면은 학습 데모 목적이라 복잡한 네비게이션 없이 `SafeAreaView` 하나에 모든 요소를 배치했다.

구성:
1. 상단 eyebrow + title + subtitle 영역
2. Conversation List 카드 — typing 사용자 수, 스키마 테이블 정보 표시
3. Chat Room 카드 — FlashList로 메시지 목록 렌더링

FlashList의 `keyExtractor`에는 `clientId`를 사용했다. 이는 pending 메시지도 고유 키를 가지도록 보장한다.

### 스타일링

프로젝트 전반의 디자인 시스템과 일관되게 warm tone 팔레트(`#f3efe8`, `#765844`, `#20150f` 등)를 적용했다. 이 스타일은 다른 study 프로젝트와 시각적 일관성을 유지하기 위한 것이다.

---

## Phase 5: 빌드 검증

### TypeScript 타입 체크

```bash
npm run typecheck
# 내부적으로 tsc --noEmit 실행
```

### 전체 검증 파이프라인

```bash
npm run verify
# typecheck + test 순차 실행
```

### Make 기반 검증

```bash
cd problem
make test        # verify_task.sh 실행 → 필수 파일 존재 확인
make app-build   # npm install + typecheck
make app-test    # npm install + jest
```

`problem/Makefile`은 `npm install --no-audit --no-fund`로 불필요한 출력을 억제하고, `node_modules`가 없을 때만 설치를 수행하도록 `test -d node_modules` 가드를 넣었다.

---

## Phase 6: 문서 정비

### docs/ 구조 작성

- `docs/concepts/README.md` — 핵심 개념 세 가지 요약
- `docs/concepts/replay-and-ack.md` — clientId/serverId 흐름과 replay dedupe 규칙
- `docs/references/README.md` — 레거시 문서 경로와 선행 프로젝트 참조

### README.md 최종 업데이트

프로젝트 루트 README에 status를 `verified`로 기재하고, 빌드/테스트 명령 세 가지를 canonical command로 고정했다.

---

## 사용한 CLI 명령 전체 요약

| 단계 | 명령 | 목적 |
|------|------|------|
| 초기화 | `npx @react-native-community/cli init` | RN 프로젝트 생성 |
| 의존성 | `npm install @nozbe/watermelondb ...` | 핵심 라이브러리 설치 |
| iOS | `cd ios && bundle install && bundle exec pod install` | 네이티브 의존성 연결 |
| 테스트 | `npm test` | Jest 실행 |
| 타입 | `npm run typecheck` | TypeScript 검증 |
| 검증 | `npm run verify` | typecheck + test |
| 빌드 | `make app-build` | Make 기반 빌드 |
| 정리 | `make clean` | node_modules, ios/build, android/build 삭제 |
