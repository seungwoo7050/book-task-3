# Native SQLite Recovery

`06`, `07`, `09`는 모두 `better-sqlite3`를 사용한다.
이 패키지는 JavaScript만으로 끝나지 않고 로컬 머신에서 native binding을 준비해야 할 수 있다.

## 언제 이 문서를 먼저 확인해야 하는가

- 새 환경에서 처음 설치할 때
- `pnpm install` 뒤에 build나 test가 바로 실패할 때
- `Could not locate the bindings file` 또는 비슷한 sqlite binding 오류가 나올 때

## 권장 설치 순서

각 구현 디렉터리에서 아래 순서로 실행한다.

1. `pnpm install`
2. `pnpm approve-builds`
3. `pnpm rebuild better-sqlite3`
4. `pnpm run build`
5. `pnpm run test`
6. e2e가 있는 프로젝트라면 `pnpm run test:e2e`

## `pnpm approve-builds`에서 무엇을 승인해야 하는가

- 이 트랙에서는 `better-sqlite3`만 승인하면 된다.
- `esbuild` 같은 다른 패키지가 보여도, 현재 이 세 프로젝트의 sqlite 복구에는 필요하지 않다.

## 자주 나오는 상황

### 1. `pnpm approve-builds`를 실행했는데 승인할 패키지가 없다고 나오는 경우

- 이전 설치에서 이미 승인된 상태일 수 있다.
- 이 경우에는 바로 `pnpm rebuild better-sqlite3`를 실행하고 build/test로 넘어간다.

### 2. `Could not locate the bindings file`가 계속 나오는 경우

- 현재 디렉터리가 맞는지 먼저 확인한다.
- 그다음 `pnpm rebuild better-sqlite3`를 다시 실행한다.
- 동일한 오류가 계속되면 `node_modules` 재설치가 필요한 환경일 수 있다.

### 3. build는 통과했는데 test/e2e에서만 sqlite 오류가 나는 경우

- 테스트가 별도 DB 초기화 경로를 타고 있을 수 있다.
- README의 실행 순서대로 같은 디렉터리에서 `build -> test -> test:e2e`를 다시 실행한다.

## 검증 기준

- `build`가 통과해야 한다.
- `test`가 통과해야 한다.
- e2e가 있는 프로젝트는 `test:e2e`까지 통과해야 native dependency 준비가 끝난 것으로 본다.

## 관련 프로젝트

- [06-persistence-and-repositories](../06-persistence-and-repositories/README.md)
- [07-domain-events](../07-domain-events/README.md)
- [09-platform-capstone](../09-platform-capstone/README.md)
