# Proving The Console Under Failure

이번 Todo에서 가장 중요했던 건 문장보다 검증 결과였다. 내부도구형 UI는 보기 좋아도 실패 순간 무너지면 신뢰를 잃는다. 그래서 이 콘솔은 typecheck, unit, integration, E2E를 모두 통과하는지와, 특히 rollback/retry/keyboard path가 실제로 이어지는지를 다시 확인하는 게 중요했다.

## 재실행 결과

```bash
$ npm run verify --workspace @front-react/ops-triage-console
```

2026-03-14 재실행 기준 결과는 다음과 같았다.

- `typecheck` 통과
- `vitest` 16개 테스트 통과
- `playwright` 4개 시나리오 통과

E2E 시나리오는 특히 좋았다.

1. detail에서 issue를 업데이트하고 undo로 되돌린다
2. saved view에서 bulk update를 적용하고 현재 `Untriaged` 필터 결과가 비는지 본다
3. simulated failure 뒤 retry가 성공하는지 본다
4. keyboard-only triage path가 끝까지 통과하는지 본다

즉 이 콘솔은 happy path만 검증하지 않는다. 실패와 회복을 제품 surface 자체의 일부로 취급한다. 다만 두 번째 시나리오는 전체 issue store가 빈다는 뜻이 아니라, 현재 saved-view filter 아래에서 더 이상 matching row가 없다는 의미다.

## integration 테스트가 list/detail/summary를 함께 묶어 준다

[`next/tests/integration/ops-triage-console.test.tsx`](/Users/woopinbell/work/book-task-3/front-react/study/frontend-portfolio/01-ops-triage-console/next/tests/integration/ops-triage-console.test.tsx)는 특히 중요했다. 여기서는 단일 mutation이

- visible row set
- detail query
- summary counters

를 동시에 바꾸는지 확인한다. 이건 내부도구에서 흔히 깨지는 부분이다. list는 바뀌었는데 detail은 옛 상태거나, summary 카운터는 늦게 따라오면 운영자는 도구를 불신하게 된다.

여기서는 failed mutation도 일부러 재현한다. `failNextRequest`를 켠 뒤 update를 보내면, toast가 `Update failed`가 되고 detail/status map이 원래 값으로 rollback되는지 본다. 그 다음 `Retry`를 눌러 실제로 성공까지 가는 경로도 고정해 둔다.

이 failure injection도 브라우저에서 `localStorage` runtime key를 바꾸는 방식이라, 테스트가 증명하는 것은 "현재 탭의 제품 surface가 rollback/retry를 버틴다"에 가깝다. 실제 backend queue, cross-session race, multi-operator overwrite는 범위 밖이다.

## 그래서 이 프로젝트의 품질 신호는 결과물보다 회복력에 가깝다

이 콘솔이 portfolio로 의미 있는 이유는 단순히 Next.js와 Tailwind를 썼기 때문이 아니다. dense data surface, optimistic update, rollback, retry, keyboard path, 발표 자료까지 하나의 제품 이야기로 묶였기 때문이다.

물론 경계도 분명하다.

- 실제 인증 없음
- 실제 DB 없음
- multi-user 협업 없음
- mock service와 local persistence 기반 데모

keyboard path 역시 같은 의미에서 읽는 편이 맞다. Playwright는 한 browser context의 한 page에서 `tabTo()` helper로 주요 포커스 흐름을 재생한다. 즉 "키보드 사용성이 있다"는 보장은 분명하지만, 여러 assistive tech 조합이나 다중 창 시나리오까지 증명한 것은 아니다.

하지만 바로 그 제한 속에서도, 내부도구가 실패와 복구를 어떻게 다뤄야 하는지는 충분히 보여 준다. 그래서 이 프로젝트는 "멋진 관리자 대시보드"보다는 "실패해도 다시 써 볼 만한 내부도구"라는 쪽으로 읽는 편이 더 정확하다.
