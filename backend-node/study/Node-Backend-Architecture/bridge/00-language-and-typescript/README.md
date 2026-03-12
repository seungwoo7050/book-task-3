# 00-language-and-typescript

- 그룹: `Bridge`
- 상태: `verified`
- 공개 답안 레인: `ts/`
- 성격: 신규 설계

## 한 줄 문제

Express와 NestJS로 넘어가기 전에 TypeScript, 비동기 흐름, 타입 모델링이 병목이 되지 않게 만드는 언어 브리지 문제다.

## 성공 기준

- `type`, `interface`, module, import/export를 직접 써서 작은 도메인 모델을 설명할 수 있다.
- `Promise`, `async/await`, 예외 처리를 테스트로 고정할 수 있다.
- CLI 입력을 파싱하고 결과를 사람이 읽을 수 있는 형태로 출력할 수 있다.

## 내가 만든 답

- `ts/`에 타입 안정성을 유지하는 작은 도서 메타데이터 처리 워크스페이스를 만들었다.
- 테스트와 CLI를 함께 두어 언어 문법, 런타임 동작, 출력 형식을 한 번에 확인하게 했다.
- 후속 프로젝트에서 반복해서 쓰는 타입 표현과 에러 처리 규약을 여기서 먼저 익히게 했다.

## 제공 자료

- `problem/README.md`
- `ts/`
- `docs/`
- `notion/`

## 실행과 검증

### TypeScript 구현
- 작업 디렉터리: `ts/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test`
- run: `pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"`

## 왜 다음 단계로 이어지는가

- `01-node-runtime-and-tooling`에서 같은 타입/에러 처리 감각을 실제 Node 런타임 입출력으로 확장한다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [ts/README.md](ts/README.md)에서 확인한다.
