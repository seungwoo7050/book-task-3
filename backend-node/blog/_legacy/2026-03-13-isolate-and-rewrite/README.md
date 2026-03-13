# backend-node blog

이 폴더는 `backend-node`의 독립 프로젝트를 `/blog/blog-writing-guide.md` 기준으로 다시 쓴 source-first 블로그 시리즈다.

- 기존 `backend-node/blog`는 존재하지 않았으므로 `isolate-and-rewrite`는 "legacy 없음 확인 후 fresh write"로 처리했다.
- 입력 근거는 `study/Node-Backend-Architecture/*/README.md`, `problem/README.md`, `docs/README.md`, 구현 레인 소스, 테스트, 실제 재검증 CLI만 사용했다.
- 각 프로젝트 폴더에는 `_evidence-ledger.md`, `_structure-plan.md`, `00-series-map.md`, `10-development-timeline.md`를 남겼다.

## Bridge

1. [00-language-and-typescript](bridge/00-language-and-typescript/00-series-map.md)
2. [01-node-runtime-and-tooling](bridge/01-node-runtime-and-tooling/00-series-map.md)
3. [02-http-and-api-basics](bridge/02-http-and-api-basics/00-series-map.md)

## Core

1. [03-rest-api-foundations](core/03-rest-api-foundations/00-series-map.md)
2. [04-request-pipeline](core/04-request-pipeline/00-series-map.md)
3. [05-auth-and-authorization](core/05-auth-and-authorization/00-series-map.md)
4. [06-persistence-and-repositories](core/06-persistence-and-repositories/00-series-map.md)
5. [07-domain-events](core/07-domain-events/00-series-map.md)

## Applied

1. [08-production-readiness](applied/08-production-readiness/00-series-map.md)
2. [09-platform-capstone](applied/09-platform-capstone/00-series-map.md)
3. [10-shippable-backend-service](applied/10-shippable-backend-service/00-series-map.md)

## 읽는 방법

1. 먼저 각 프로젝트의 `00-series-map.md`에서 질문, source-of-truth, 대표 검증 경로를 잡는다.
2. `10-development-timeline.md`에서 실제 파일 순서와 테스트 신호가 어떻게 이어졌는지 따라간다.
3. 복원 근거가 더 필요하면 `_evidence-ledger.md`와 `_structure-plan.md`를 본다.
