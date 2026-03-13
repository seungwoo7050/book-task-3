# 04-request-pipeline evidence ledger

이 프로젝트 역시 `git log`는 `2026-03-12` 한 번의 이관 커밋으로 압축돼 있다. chronology는 middleware, filter/interceptor, e2e 테스트, 재검증 CLI를 기준으로 다시 세웠다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | validation을 handler 밖의 공통 단계로 뺀다 | `express/src/middleware/validate.ts` | controller에서 if문으로 검사해도 충분해 보였다 | Zod 기반 `validate(schema)`를 만들어 body parsing 뒤 검증을 pipeline으로 고정했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` (`express/`) | `Tests 16 passed`, `test:e2e 9 passed` | `req.body = schema.parse(req.body)` | validation이 밖으로 빠지면 handler는 검증된 값만 받는다는 전제를 가질 수 있다 | 응답 표면도 같은 방식으로 묶어야 한다 |
| 2 | Phase 2 | 성공/실패 응답의 모양을 통일한다 | `express/src/middleware/response-wrapper.ts`, `error-handler.ts` | 성공 응답만 감싸도 충분할 것 같았다 | 성공은 `{ success: true, data }`, 실패는 `{ success: false, error }`로 나누고 malformed JSON도 같은 규약에 넣었다 | 같은 명령 재실행 | missing book, invalid type, negative price, malformed JSON이 모두 표준 error envelope로 돌아온다 | `res.json = function (body?: unknown): Response { ... }` | response shaping은 미관보다도 애플리케이션 전체의 관찰 표면을 고정하는 일에 가깝다 | NestJS에서도 같은 규약을 다시 세운다 |
| 3 | Phase 3 | NestJS에서 같은 규약을 global pipeline으로 재현한다 | `nestjs/src/common/filters/http-exception.filter.ts`, `transform.interceptor.ts` | 프레임워크가 다르면 기본 응답 형식도 달라질 수밖에 없을 것 같았다 | global `ValidationPipe`, filter, interceptor를 조합해 Express와 거의 같은 계약을 만들었다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` (`nestjs/`) | `Tests 7 passed`, `test:e2e 8 passed` | `response.status(status).json({ success: false, error: ... })` | pipeline은 feature 바깥 옵션이 아니라 이후 모든 feature가 의존하는 바닥 규약이다 | 다음 프로젝트에서 이 규약 위에 JWT와 RBAC를 올린다 |

## 근거 파일

- `core/04-request-pipeline/README.md`
- `core/04-request-pipeline/problem/README.md`
- `core/04-request-pipeline/express/src/middleware/validate.ts`
- `core/04-request-pipeline/express/src/middleware/response-wrapper.ts`
- `core/04-request-pipeline/express/src/middleware/error-handler.ts`
- `core/04-request-pipeline/nestjs/src/common/filters/http-exception.filter.ts`
- `core/04-request-pipeline/nestjs/src/common/interceptors/transform.interceptor.ts`
- `core/04-request-pipeline/express/test/e2e/pipeline.e2e.test.ts`
- `core/04-request-pipeline/nestjs/test/e2e/pipeline.e2e.test.ts`
