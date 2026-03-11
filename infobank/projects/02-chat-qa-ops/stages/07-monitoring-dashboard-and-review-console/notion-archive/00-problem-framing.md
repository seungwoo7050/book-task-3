> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Monitoring Dashboard — 문제 정의

## 풀어야 하는 문제

stage 06까지 만든 파이프라인은 CLI에서만 실행 가능하다.
golden set 결과도 JSON으로 출력되고, version compare도 터미널에서만 볼 수 있다.

운영 팀이 매일 확인해야 하는 정보:
1. 전체 평균 점수와 등급 분포
2. 어떤 failure_type이 가장 많이 발생하는지
3. 개별 상담 세션의 상세 평가 결과
4. 새 버전이 기존 버전보다 나은지

이걸 매번 코드를 실행해서 확인하는 건 비현실적이다.
**웹 대시보드**가 필요하다.

## snapshot API 접근

실시간 데이터를 제공하려면 DB 연결, 쿼리 최적화, 캐싱이 필요하다.
stage 수준에서는 이게 과하다.

대신 **snapshot 방식**을 선택했다:
- 모든 API가 하드코딩된 SNAPSHOT dict에서 데이터를 반환한다
- DB 없이 API 계약(request/response schema)을 먼저 확정한다
- React 프론트엔드는 이 API에 맞춰 개발한다
- capstone에서 실제 DB로 교체할 때, API schema만 같으면 프론트엔드 수정이 불필요하다

이건 "fake it till you make it"이 아니라 **interface-first 설계**다.
API 계약이 먼저 확정되면, 백엔드와 프론트엔드를 독립적으로 개발할 수 있다.

## 대시보드의 4가지 뷰

| 페이지 | 경로 | 표시 내용 |
|--------|------|-----------|
| 개요(Overview) | `/` | 평균 점수, 실패율, critical 건수, 등급 분포, version compare |
| 실패 분석(Failures) | `/failures` | failure_type별 발생 건수, critical 비율, 평균 점수 |
| 세션 리뷰(SessionReview) | `/sessions` | 개별 상담 세션 목록, 상세 턴/평가 조회 |
| 평가 실행(EvalRunner) | `/runner` | golden set 실행 트리거, 결과 표시 |
