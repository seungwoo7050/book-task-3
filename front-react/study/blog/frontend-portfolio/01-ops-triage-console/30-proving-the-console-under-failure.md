# Proving The Console Under Failure

좋은 internal tool을 설명할 때 가장 설득력이 떨어지는 장면은 모든 것이 순조롭게만 흘러가는 데모다. 실제 운영자는 저장 실패도 겪고, 느린 응답도 겪고, 마우스 없이도 화면을 통과해야 한다. 그래서 Ops Triage Console의 마지막 증명은 happy path가 아니라 failure surface를 보여 주는 쪽으로 향했다.

이 글에서 중요한 건 코드를 더 많이 붙였다는 사실이 아니다. 이미 만든 surface와 reversible mutation이 실제 실패와 재시도와 keyboard path 앞에서 무너지지 않는다는 것을 어떻게 검증했는가가 핵심이다.

## 구현 순서를 먼저 짚으면

- failure simulation을 별도 helper로 떼어, 안정 모드와 chaos-like 모드를 명시적으로 다뤘다.
- Playwright에서 undo, bulk update, retry, keyboard-only path를 실제 사용 흐름으로 재생했다.
- 마지막 verify는 typecheck, unit/integration, e2e를 한 번에 묶어 포트폴리오 품질 신호로 만들었다.

## 실패는 숨기지 않고 코드로 드러냈다

`simulate.ts`를 보면 이 프로젝트가 failure를 우연한 외부 변수로 두지 않았다는 사실이 드러난다. "이번 요청만 실패"와 "일정 비율로 실패"를 runtime config로 직접 제어한다.

```ts
export function shouldSimulateFailure(
  config: DemoRuntimeConfig,
  randomValue = Math.random(),
): boolean {
  if (config.failNextRequest) {
    return true;
  }
  if (config.mode === "stable") {
    return false;
  }
  return randomValue < config.failureRate;
}
```

실패도 그냥 generic error가 아니다. retryable error를 명시적으로 만들고, UI는 그 성격을 surface로 끌어올린다.

```ts
export function createRetryableError(): DemoServiceError {
  const error = new Error("Transient failure. Retry the request.") as DemoServiceError;
  error.code = "DEMO_TRANSIENT_FAILURE";
  error.retryable = true;
  return error;
}
```

이 덕분에 retry는 데모용 버튼이 아니라 설계된 동작이 된다. 사용자는 "실패했다"는 문장 대신 "지금 이 실패는 다시 시도할 수 있는 종류다"라는 힌트를 받는다.

## 마지막에는 브라우저 시나리오로 operator의 움직임을 그대로 재생했다

Playwright 시나리오를 보면 이 프로젝트가 무엇을 품질 기준으로 삼는지 아주 선명하다. undo, bulk update, retry, keyboard-only triage가 각각 독립된 테스트 이름으로 남아 있다.

```ts
test("surfaces a simulated write error and retries successfully", async ({ page }) => {
  await page.evaluate(() => {
    window.localStorage.setItem(
      "ops-triage-console:runtime",
      JSON.stringify({
        latencyMs: 220,
        failureRate: 0,
        failNextRequest: true,
        mode: "stable",
      }),
    );
  });
  ...
  await expect(page.getByText("Update failed")).toBeVisible();
  await page.getByRole("button", { name: "Retry" }).click();
  await expect(page.getByText("Issue updated")).toBeVisible();
});
```

이건 테스트 이름만 멋있게 붙인 것이 아니다. operator가 실제로 겪는 실패와 회복 경로를 그대로 surface에 옮긴 것이다. keyboard-only path도 마찬가지다. 검색 input에 탭으로 도달하고, 행을 열고, note를 입력하고, triage를 적용하는 흐름이 별도 시나리오로 남아 있다.

```ts
test("supports a keyboard-only triage path", async ({ page }) => {
  const searchInput = page.getByTestId("issue-search");
  await tabTo(page, searchInput);
  await page.keyboard.type("search results disappear");
  ...
  await page.keyboard.press("Enter");
  await expect(page.getByText("Issue updated")).toBeVisible();
});
```

즉 이 프로젝트의 e2e는 화면이 예쁘게 뜨는지 보는 스모크 테스트가 아니다. internal tool이 실제 운영 환경의 불편한 순간들을 견딜 수 있는지 확인하는 증명에 가깝다.

## verify가 포트폴리오 신호가 되는 이유

이 앱은 verify를 꽤 무겁게 가져간다.

```bash
cd study
npm run verify --workspace @front-react/ops-triage-console
```

2026-03-13 replay 기준으로 typecheck가 통과했고, `vitest` 16개와 Playwright 4개 시나리오가 모두 통과했다. 숫자 자체보다 중요한 건 범위다. 타입 안정성, optimistic/cache consistency, failure simulation, operator e2e path가 한 묶음으로 돌아간다.

그래서 이 프로젝트는 "내부도구를 만들 수 있다"보다 한 단계 더 나아간다. 내부도구를 어떤 실패 조건 아래서도 설명 가능한 결과물로 남길 수 있다는 사실을 보여 준다.

## 무엇이 아직 남았는가

여전히 이 앱은 mock API와 local persistence를 기반으로 한 데모다. 실제 인증, 실제 DB, 멀티유저 협업은 범위 밖에 있다. 하지만 internal tool로서 가장 중요한 신뢰의 핵심은 이미 드러났다. 빠르게 바뀌는 화면이어도, 실패했을 때 rollback과 retry가 보이고, keyboard path도 살아 있어야 한다는 사실이다.

다음 프로젝트는 같은 포트폴리오 트랙 안에서도 시선이 달라진다. `Client Onboarding Portal`은 operator가 아니라 고객이 통과해야 하는 flow를 다루기 때문에, 밀도보다 연속성과 복원성이 더 중요한 문제로 올라온다.
