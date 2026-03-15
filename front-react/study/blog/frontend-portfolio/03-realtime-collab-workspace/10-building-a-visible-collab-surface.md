# Building A Visible Collab Surface

협업 앱을 만들 때 가장 먼저 빠지기 쉬운 함정은 sync engine을 먼저 떠올리는 것이다. 하지만 이 프로젝트를 실제로 읽어 보면 첫 번째 결정은 알고리즘이 아니라 배치였다. `WorkspaceShell`은 board cards, doc blocks, presence rail, activity log, conflict banner를 한 화면에 모두 올린다. 그 이유는 단순하다. "지금 무엇이 바뀌었고, 누가 있었고, 이 값이 믿을 만한가"를 사용자가 같은 시야에서 읽을 수 있어야 하기 때문이다.

문제 정의도 이 방향을 분명히 말한다. 요구 범위는 shared board cards, shared doc blocks, collaborator presence, optimistic patch apply, reconnect replay, conflict banner, activity log다. 즉 collaboration feel을 만드는 요소를 숨은 상태 모델로 두지 말고 제품 surface로 드러내라는 요구다. 이 프로젝트는 그 요구를 UI 배치에서부터 받아들였다.

## 첫 번째 설계 전환점은 편집 surface와 협업 상태를 떼지 않는 것이었다

`workspace-shell.tsx`의 hero/status 구역은 단순 요약판이 아니다. viewer, connection, queued patch count, conflict count를 편집 surface보다 먼저 보여 준다.

```tsx
<div className="status-card">
  <span className="muted">Connection</span>
  <strong data-testid="connection-status">
    {state.connection === "connected" ? "Connected" : "Disconnected"}
  </strong>
</div>
<div className="status-card">
  <span className="muted">Queued patches</span>
  <strong data-testid="queued-count">{state.queuedPatches.length}</strong>
</div>
```

이 선택이 중요한 이유는 협업 앱의 핵심 정보를 편집 결과 뒤에 숨기지 않기 때문이다. 사용자는 "카드 값이 바뀌었다"만 보는 게 아니라, 그 값이 지금 연결된 상태에서 생긴 것인지, 오프라인 queue가 남아 있는지까지 같은 문맥에서 본다.

같은 원리가 conflict에도 적용된다. 충돌은 작은 toast가 아니라 상단 배너다.

```tsx
{state.conflicts.bannerVisible ? (
  <section className="banner" data-testid="conflict-banner" role="alert">
    <p>{state.conflicts.message}</p>
    <button onClick={dismissConflict} type="button">
      Dismiss
    </button>
  </section>
) : null}
```

즉 이 앱은 overwrite를 조용히 삼키지 않는다. 협업의 불편한 순간을 제품 surface에 남겨서, 다른 사람이 UI만 보고도 현재 sync 모델의 한계를 설명할 수 있게 한다.

## board와 doc는 다른 화면이지만 같은 patch envelope를 공유한다

겉으로는 board card input과 doc textarea가 다른 위계를 갖지만, 실제 runtime에서 두 surface는 같은 계약을 공유한다. 둘 다 `setCardTitle()` 또는 `setDocText()`를 거쳐 `sendPatch()`로 들어가고, वहां `createPatchEnvelope()`로 같은 patch shape를 만든다.

그래서 이 프로젝트는 "보드 기능"과 "문서 기능"을 따로 설명하지 않는다. 더 중요한 질문은 서로 다른 UI가 같은 sync 규칙을 공유하는가다. `workspace-state.ts`도 이걸 그대로 반영한다. `PatchEnvelope`는 `entityType`, `entityId`, `field`, `value`만 바뀔 뿐이고, `applyPatchToState()`가 card/doc를 같은 흐름으로 태운다.

이 구조 덕분에 문서 편집이 특별 취급되지 않는다. 현재 구현이 rich text merge나 CRDT를 다루지 않는다는 한계도 더 선명해진다. doc는 특별한 엔진이 아니라 block-level patch surface다.

## presence와 activity는 부가 패널이 아니라 신뢰 장치다

presence list와 activity log는 "있으면 좋은 협업 장식"이 아니다. 현재 sync 상태를 설명하는 두 축이다.

- presence: 지금 누가 살아 있는지, online/offline이 어떤 참가자에게 붙는지 보여 준다.
- activity: local patch, remote patch, queued replay 같은 사건을 시간축으로 남긴다.

특히 activity는 `useDeferredValue(state.activity)`를 써서 편집 감각을 해치지 않으면서도 최근 사건을 유지한다. 이건 작은 선택이지만, collab shell이 편집성과 설명 가능성을 같이 챙기려 했다는 신호다.

## 이 표면 덕분에 무엇이 보이고, 무엇이 아직 안 보이는가

현재 surface는 꽤 솔직하다. connection, queued patch, conflict count, presence, activity가 모두 보인다. 반면 durable server log, per-field merge reason, cursor position, selection broadcast는 안 보인다. 소스도 그 한계를 숨기지 않는다. `BroadcastChannelTransport`와 `MemoryCollabTransport`만 있고, conflict는 banner 하나로 정리된다.

이 문서의 결론은 단순하다. 이 프로젝트의 첫 승부는 sync engine을 복잡하게 만드는 데 있지 않았다. 협업 상태를 읽을 수 있는 화면을 먼저 고정한 데 있었다. 그다음 글에서는 그 화면 뒤에서 optimistic patch, queue, replay, presence heartbeat가 실제로 어떻게 이어지는지 본다.
