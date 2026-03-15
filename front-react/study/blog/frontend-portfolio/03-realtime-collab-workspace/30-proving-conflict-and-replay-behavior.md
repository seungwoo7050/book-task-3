# Proving Conflict And Replay Behavior

협업 데모는 종종 "로컬에서 잘 보였다"는 말로 끝난다. 이 프로젝트가 괜찮은 이유는 그 지점에서 멈추지 않기 때문이다. unit test는 state transition을 고정하고, integration test는 UI shell이 transport event에 반응하는지 확인하며, Playwright는 실제 두 탭에서 presence, replay, conflict banner를 다시 밟는다. 즉 코드가 약속한 mental model을 검증이 거의 같은 문장으로 반복해 준다.

## unit test는 state machine의 핵심 전이를 고정한다

`workspace-state.test.ts`가 고정하는 것은 네 가지다.

- optimistic local patch가 즉시 board에 반영되는가
- remote heartbeat가 presence를 갱신하는가
- offline queue가 reconnect flush 뒤 비워지는가
- overlapping edit에서 conflict banner가 올라오고 dismiss가 가능한가

이 네 조합이 중요한 이유는 hook 내부 동작을 UI보다 먼저 최소 단위로 고정해 주기 때문이다. 특히 `queuePatch()`와 `flushQueuedPatches()`가 따로 검증되기 때문에 reconnect 설명이 "느낌상 되는 것 같다" 수준에 머물지 않는다.

## integration test는 visible shell이 정말 같은 규칙을 드러내는지 확인한다

`realtime-collab-workspace.test.tsx`는 `MemoryCollabTransport`를 주입해서 deterministic하게 shell을 확인한다. 로컬 input 변경 후 값이 바로 바뀌는지, remote presence가 들어오면 list에 Rio가 보이는지, remote overwrite 후 alert 배너가 뜨는지, activity log에 `Remote card patch`가 남는지를 본다.

이 테스트가 중요한 이유는 unit test와 E2E 사이를 메워 주기 때문이다. transport 구현체가 실제 `BroadcastChannel`이 아니어도 product shell이 무엇을 보여 줘야 하는지는 충분히 검증할 수 있다. 즉 visible collaboration surface라는 이 프로젝트의 주제가 integration 테스트에도 직접 연결된다.

## E2E는 실제 두 탭에서 presence, replay, conflict를 다시 밟는다

2026-03-14에 다시 돌린 canonical verification은 아래 한 줄이다.

```bash
cd /Users/woopinbell/work/book-task-3/front-react/study
npm run verify --workspace @front-react/realtime-collab-workspace
```

이번 재실행에서 확인한 사실은 다음과 같다.

- `typecheck`: 통과
- `vitest`: 2개 파일, 5개 테스트 통과
- `playwright`: 2개 시나리오 통과

E2E 두 개는 각각 역할이 분명하다.

1. `syncs board edits and presence across two pages`
   - atlas와 rio 두 탭을 띄운다.
   - atlas presence list에 Atlas와 Rio가 모두 잡히는지 본다.
   - atlas에서 `card-1`을 수정하면 rio에서도 같은 값이 보이는지 확인한다.
2. `replays queued patches after reconnect and surfaces conflicts`
   - atlas를 disconnect한 뒤 `card-2`를 수정한다.
   - 이 값이 reconnect 전에는 rio에 반영되지 않는지 본다.
   - reconnect 후 queued patch가 rio에 전달되는지 본다.
   - 같은 `card-1`을 atlas/rio가 다르게 수정하면 atlas에서 conflict banner가 뜨는지 확인한다.

즉 이 프로젝트의 realtime claim은 추상적인 말이 아니다. "두 탭 간 sync", "offline queue 후 replay", "overlapping overwrite 배너"라는 세 문장으로 바로 재현 가능하다.

다만 이 claim도 테스트 장비 수준까지 정확히 적어야 한다. Playwright는 두 개의 완전히 다른 기기가 아니라 같은 browser context 안의 두 페이지를 띄우고, transport 기본 구현도 same-origin `BroadcastChannel`이다. 따라서 현재 자동 검증이 직접 잠그는 것은 "같은 브라우저 안 두 탭 협업"까지이지, cross-device/server-mediated realtime 전체는 아니다.

## 검증이 고정하지 않는 경계도 함께 남긴다

이번 verify는 모두 통과했지만, 소스 기준으로 아직 고정하지 않는 경계도 분명하다.

- remote patch ordering에 대한 durable server arbitration은 없다.
- queue replay 성공 여부를 ack로 확인하지 않는다.
- `BroadcastChannel`이 없는 환경 fallback transport는 없다.
- conflict는 entity overwrite를 보여 줄 뿐, text merge나 resolution workflow를 제공하지 않는다.

또 `vitest` 실행 중 Vite deprecation warning이 출력된다. 현재는 non-blocking warning이지만, tooling surface가 완전히 정돈된 상태는 아니라는 신호다.

그래서 이 capstone의 진짜 강점은 "완벽한 협업 엔진"이 아니라 "어떤 협업 상태를 현재 구현이 책임지고, 무엇은 아직 책임지지 않는가"를 코드와 테스트가 함께 설명해 준다는 점이다. 포트폴리오 문서로서도 이 편이 훨씬 설득력이 있다.
