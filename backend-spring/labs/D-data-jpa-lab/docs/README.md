# D-data-jpa-lab Notes

## Implemented now

- Flyway-managed `lab_products` table
- JPA entity, repository, and service boundary
- page-based listing and optimistic-lock-style version check

## Important simplifications

- Querydsl is installed but not exercised deeply yet
- soft delete is still a documented extension point
- the API covers one core aggregate instead of a larger catalog graph

## Next improvements

- add Querydsl search conditions and sort combinations
- introduce category and review tables
- add soft delete and N+1 regression tests
