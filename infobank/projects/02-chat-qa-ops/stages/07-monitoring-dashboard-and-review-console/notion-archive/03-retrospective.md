> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Monitoring Dashboard — 회고

## 잘 된 것

### snapshot 방식이 API 계약 확정에 효과적이다

DB 없이 SNAPSHOT dict만으로 API를 구현했더니,
API schema 논의가 빠르게 끝났다.
프론트엔드 개발자는 API 문서 대신 SNAPSHOT dict를 읽으면 된다.

### 프론트엔드와 백엔드의 완전한 분리

React 앱은 `/api/*` 경로로만 통신한다.
백엔드가 snapshot에서 실제 DB로 바뀌어도, 응답 형태만 같으면 프론트엔드는 수정할 필요가 없다.
실제로 capstone v0→v1 전환에서 이 분리가 검증되었다.

### lineage 추적이 대시보드에 내장됨

세션 상세 뷰에서 각 평가의 lineage(run_label, dataset, trace_id, retrieval_version)를 바로 볼 수 있다.
문제가 생겼을 때 "이 평가는 어떤 조건에서 실행되었는가"를 즉시 확인할 수 있다.

## 아쉬운 것

### 실시간 데이터가 없다

snapshot은 정적이다. 새 상담이 들어와도 대시보드가 갱신되지 않는다.
capstone에서 DB 연결 후에야 실시간 반영이 가능하다.

### 대시보드 접근 제어가 없다

현재 누구나 API에 접근할 수 있다.
capstone v3에서 auth/RBAC가 추가되지만, 이 stage에서는 고려하지 않았다.
