# 접근 과정: 요청의 생명주기를 직접 설계하다

## AsyncState: boolean 하나로는 부족하다

처음에는 `isLoading: boolean` 하나로 충분히 될 줄 알았다. 하지만 실제로 UI를 만들어 보니, "로딩 중"과 "에러"와 "결과가 없음"은 사용자에게 완전히 다른 의미다.

그래서 `AsyncState` 타입을 `"idle" | "loading" | "success" | "empty" | "error"`로 나눴다. 이 다섯 가지 상태 각각에 다른 UI를 보여 준다:

- **idle**: 초기 상태, 아직 요청을 보내지 않은 상태
- **loading**: 목록이나 상세를 가져오는 중. "Loading directory…" 텍스트 표시
- **success**: 결과가 있음. 목록 또는 상세 내용 표시
- **empty**: 요청은 성공했지만 결과가 없음. "No matching results" 안내
- **error**: 요청이 실패함. 에러 메시지와 Retry 버튼 표시

특히 **empty와 error의 구분**이 중요했다. empty는 사용자의 쿼리가 결과를 만들지 못한 것이고, error는 시스템이 응답하지 못한 것이다. 사용자에게 "검색어를 바꿔 보세요"라고 말할 것인지, "다시 시도해 주세요"라고 말할 것인지가 달라진다.

## 목록과 상세의 상태 분리

이 앱에는 목록(list)과 상세(detail)라는 두 개의 비동기 흐름이 있다. 처음에는 하나의 `asyncState`로 관리하려 했지만, 목록은 성공했는데 상세만 로딩 중인 상태를 표현할 수 없었다.

그래서 `listState`와 `detailState`를 분리했다. 각각 독립적으로 loading, success, error를 가질 수 있다. 예를 들어:
- 목록을 검색해서 성공 → `listState: "success"`
- 항목을 클릭해서 상세를 로드 중 → `detailState: "loading"`
- 상세 로드 실패 → `detailState: "error"`, 목록은 여전히 보임

이 분리 덕분에 "목록은 보이는데 상세가 로딩 중"이라는 정상적인 상태를 자연스럽게 표현할 수 있게 됐다.

## AbortController: 이전 요청을 취소하다

검색창에 글자를 타이핑하면, 글자마다 `loadList()`가 호출된다. 만약 이전 요청이 아직 도착하지 않았는데 새 요청이 나가면 어떻게 될까? 이전 응답이 나중에 도착해서 새 검색 결과를 덮어쓸 수 있다.

해결은 **AbortController**다.

```typescript
const loadList = async () => {
  listController?.abort();               // 이전 요청 취소
  listController = new AbortController(); // 새 컨트롤러 생성
  // ...
  await service.listDirectory(query, listController.signal);
};
```

새 요청이 시작될 때마다 이전 AbortController를 abort()하고 새로 만든다. mock service의 `wait()` 함수는 signal의 abort 이벤트를 듣고 있어서, 취소되면 즉시 `AbortError`를 던진다.

## requestTracker: 응답 순서를 보장하다

AbortController만으로는 충분하지 않다. abort()가 호출되더라도 이미 응답이 오고 있는 중이면 catch되지 않을 수 있다. 그래서 **request token** 패턴을 추가했다.

```typescript
const tracker = createRequestTracker();
const token = tracker.next();
// ... 요청 ...
if (!tracker.isLatest(token)) return; // 내가 최신 요청이 아니면 무시
```

`createRequestTracker()`는 호출할 때마다 증가하는 숫자를 반환하고, `isLatest()`로 그 숫자가 아직 최신인지 확인한다. AbortController가 요청을 물리적으로 취소하고, tracker가 논리적으로 오래된 응답을 무시하는 이중 안전장치다.

## Simulate Failure: 의도적 실패

실패 시나리오를 테스트하기 위해 "Simulate next request failure" 버튼을 만들었다. 이 버튼을 누르면 `simulateFailureNext` 플래그가 설정되고, 다음 목록 요청이 반드시 실패한다. 실패 후에는 에러 UI와 Retry 버튼이 나타나고, Retry를 누르면 플래그가 해제되어 정상 요청이 돌아간다.

이 패턴은 실무에서 서버 장애를 시뮬레이션할 때도 유용하지만, 무엇보다 **개발 중에 에러 UI를 반복적으로 확인**할 수 있게 해 준다. 서버를 실제로 끄지 않아도 에러 상태를 만들 수 있다.

## 포커스 관리의 반복

이전 프로젝트에서도 겪었던 문제가 여기서도 반복됐다. `container.innerHTML`을 교체하면 포커스가 사라진다. 검색창에 타이핑하는 중에 DOM이 교체되면 커서가 없어지고, 에러 후 Retry 버튼을 눌러야 하는데 포커스가 어딘가로 사라진다.

각 상태 전이마다 `focusSelector`를 명시적으로 넘겨서 render 후에 focus를 복원했다. 이 패턴이 세 번째로 반복되니, "이건 프레임워크가 자동으로 해 줘야 하는 일"이라는 확신이 더 강해졌다.
