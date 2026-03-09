# Runbook

## Demo Scenario

역할:

- owner: 팀 접근과 설정 관리
- operator: 추천, compare, gate 실행
- viewer: 결과 확인만 수행

상황:

한 팀이 `release-check-bot@1.5.0`을 self-hosted 환경에서 운영하고 있다. owner가 팀 접근을 정리하고, operator가 compare/release gate를 돌린 뒤, viewer가 결과만 확인한다.

## Steps

1. owner 로그인
2. `Team Access`에서 operator 또는 viewer를 추가
3. `Catalog Import/Export`에서 bundle을 export하거나 import
4. `Candidate 실행`으로 추천 근거 확인
5. `Compare Job`, `Compatibility Job`, `Release Gate Job` 순서로 실행
6. `Artifact Export Job`으로 최신 Markdown artifact 생성
7. viewer로 재로그인해 read-only 화면과 artifact preview 확인

## Operator Checks

- `Job Activity`에 최근 상태가 남는가
- `Proof Snapshot`이 기대 값에 맞는가
- `Latest Artifact Preview`가 비어 있지 않은가
- `Audit Log`에 owner/operator action이 남는가
