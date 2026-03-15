# 00-language-and-typescript Evidence Ledger

## 독립 Todo 판정
- 판정: `done`
- 이유: `problem/README.md`가 별도 성공 기준을 가진 독립 bridge 문제이고, `ts/` 워크스페이스가 이 프로젝트만의 build/test/CLI surface를 갖는다.
- 이번 Todo에서도 기존 blog 본문은 입력 근거로 사용하지 않았다.

## 이번 턴에 읽은 근거
- `backend-node/README.md`
- `backend-node/problem-subject-elective/README.md`
- `backend-node/study/Node-Backend-Architecture/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/problem/script/run-example.sh`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/package.json`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/catalog.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/src/cli.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/tests/catalog.test.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/docs/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/docs/concepts/type-modeling.md`

## 소스에서 확인한 핵심 사실
- 이 프로젝트의 주제는 문법 나열이 아니라 입력 정규화와 오류 계약이다.
- `BookDraft`와 `NormalizedBook`이 분리돼 있어 외부 입력과 내부 신뢰 상태를 다르게 다룬다.
- tags는 trim/lowercase/slugify/dedupe/sort를 한 번에 거친다.
- summary는 description이 비어 있으면 자동 문장으로 fallback 된다.
- inventory 조회는 helper 수준에서만 구현돼 있으며, 항목 단위 `error`를 가진 결과 배열로 실패를 흡수한다.
- 실제 CLI는 inventory 조회를 호출하지 않기 때문에 출력은 `Inventory: not requested`로 끝난다.
- `parseArgs()`는 필수 플래그 누락 시 명시적 오류를 던지고, `runCli()`는 stderr와 exit code로 변환한다.
- 연도 검증은 `publishedYear < 0`만 막아서 `0`을 허용하지만, 오류 메시지는 "positive integer"라고 써 있어 경계 표현이 완전히 일치하지 않는다.
- `problem/script/run-example.sh`는 `ts/`로 `cd`하지 않아서 상위 폴더에서 그대로 실행하면 실패한다.

## 검증 명령과 실제 결과

| 명령 | 결과 | 메모 |
| --- | --- | --- |
| `pnpm run build` | 통과 | `tsc` exit code `0`, compiler error 없음 |
| `pnpm run test` | 통과 | `1` file, `6` tests passed |
| `pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"` | 통과 | `Slug: node-patterns-2024`, `Tags: architecture, node`, `Inventory: not requested` 출력 확인 |
| `bash problem/script/run-example.sh` | 실패 | 상위 폴더 실행 시 `ERR_PNPM_NO_IMPORTER_MANIFEST_FOUND`, `package.json`을 찾지 못함 |

## 이번 문서가 기대는 중심 앵커
- 정규화 경계 앵커: `ts/src/catalog.ts`
- CLI 계약 앵커: `ts/src/cli.ts`
- 테스트 앵커: `ts/tests/catalog.test.ts`
- 개념 언어 앵커: `docs/concepts/type-modeling.md`

## 이번 턴의 품질 메모
- "TypeScript 입문"이 아니라 이후 Node 프로젝트들이 계속 재사용할 입력/오류 계약의 출발점으로 다시 썼다.
- async inventory helper가 실제 CLI까지 연결된 것처럼 과장하지 않았다.
- 실제 재현 스크립트의 현재 cwd 가정 실패까지 검증 결과에 포함했다.
