# Knowledge Index

## Reusable concepts

- Entity versus service boundary:
  - JPA entity에 모든 규칙을 밀어 넣지 않고 application/service layer와 역할을 나누는 사고다.
- Flyway plus JPA:
  - 스키마 진화와 ORM 매핑을 함께 관리하는 방식이다.
- Optimistic locking:
  - version 기반 충돌 감지로 stale update를 막는 패턴이다.

## Glossary

- N+1:
  - 목록 조회 후 연관 데이터를 개별 쿼리로 반복 로드하는 비효율이다.
- Querydsl:
  - type-safe query construction을 위한 도구다.

## References

- title:
  - D-data-jpa-lab Notes README
  - URL or local path: `/Users/woopinbell/work/web-pong/study2/labs/D-data-jpa-lab/docs/README.md`
  - checked date: `2026-03-09`
  - why it was consulted: current scope와 부족한 점을 맞추기 위해 확인했다
  - what was learned: Querydsl은 설치됐지만 아직 deeply exercised되지는 않는다
  - what changed: 디버그 로그와 회고에서 keyword inflation을 경계하는 문장을 넣었다
