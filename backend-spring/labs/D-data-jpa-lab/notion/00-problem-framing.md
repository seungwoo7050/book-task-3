# Problem Framing

## Goal

`study2/labs/D-data-jpa-lab`의 목표는 JPA를 단순 CRUD helper가 아니라 설계 선택이 드러나는 도구로 다루는 것이다. product/category/review 스타일 CRUD, Querydsl search, pagination, optimistic locking, N+1 awareness는 “Spring Data JPA를 쓸 줄 안다”는 말을 더 구체적인 문제로 바꾼다. 최소 성공 조건은 현재 scaffold 범위 안에서 entity, repository, service boundary, version check가 검증되고, deeper Querydsl/N+1 work는 후속 과제로 남긴다는 점이 명확한 것이다.

## Inputs and constraints

- Java/Spring:
  - Java 21
  - Spring Boot 3.4.x
  - Spring Data JPA + Querydsl
- Datastores:
  - Flyway-managed relational schema
- Correctness requirements:
  - CRUD
  - pagination and sorting
  - optimistic locking
- Repository givens:
  - current scope는 one core aggregate 중심
- Decisions still needed:
  - Querydsl을 얼마나 일찍 실제 검색에 넣을지

## Success criteria

- JPA entity와 service boundary가 분리되어야 한다.
- pagination과 optimistic lock semantics가 설명 가능해야 한다.
- documented commands가 통과해야 한다.
- soft delete, richer search, N+1 regression은 아직 다음 단계라는 점을 명시해야 한다.

## Uncertainty log

- Querydsl을 설치해도 실제 query complexity가 적으면 학습 효과가 약할 수 있다.
- 그래도 scaffold 단계에서는 JPA 구조와 optimistic locking을 먼저 굳히는 편이 낫다고 가정했다.
- deeper search와 N+1 regression은 후속 보강이 필요하다.

