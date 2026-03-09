# Debug Log

## Current recorded issue

이 랩의 현재 문제는 런타임 버그보다 구현 깊이와 문서 설명의 간극이다.

- failing command or request:
  - none recorded as a blocking defect in the current pass
- exact symptom:
  - organization creation, invite, role change가 동작해도 Spring method security가 아직 없으면 authorization lab이 과장되어 보일 수 있다
- first incorrect assumption:
  - RBAC surface만 있으면 authorization 구현이 충분히 깊어 보일 것이라고 생각하기 쉽다
- evidence collected:
  - docs는 membership state가 in memory이고 method security가 next improvement라고 적는다

## Root cause

authorization 문제는 API surface보다 enforcement 위치가 중요하다. 현재 scaffold는 service logic 중심이라, declarative policy까지는 아직 가지 않았다.

## Fix and verification

- code or config change made:
  - tracked docs에서 current implementation과 next improvements를 분리했다
- why that change addresses the cause:
  - 독자가 실제 enforcement depth를 과대평가하지 않는다
- command, test, or log line that proved the fix:
  - `make test`
  - `make smoke`

## Follow-up debt

- forbidden-path tests를 더 늘릴 수 있다
- method annotation 기반 enforcement를 실제로 옮겨야 한다

