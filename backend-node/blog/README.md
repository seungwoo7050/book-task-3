# backend-node blog

이 폴더는 `backend-node` 트랙을 코드와 검증 기록 중심으로 다시 읽어 낸 블로그 묶음이다. 예전 초안은 [`_legacy/2026-03-13-isolate-and-rewrite`](./_legacy/2026-03-13-isolate-and-rewrite)에 따로 보관했고, 지금 보이는 문서는 소스코드, 테스트, README, 실제 재검증 CLI만 근거로 다시 쓴 버전이다.

읽는 흐름은 단순하다. 각 프로젝트의 `00-series-map.md`에서 "이걸 왜 읽어야 하는지"를 먼저 잡고, `10-development-timeline.md`에서 구현 순서를 따라간다. chronology를 더 촘촘히 확인하고 싶을 때만 `_evidence-ledger.md`와 `_structure-plan.md`로 내려가면 된다.

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

## 이 시리즈를 읽는 기준

- `bridge`는 문법 복습이 아니라, 이후 모든 프로젝트가 기대하는 입력·출력 계약을 세우는 구간이다.
- `core`는 같은 문제를 Express와 NestJS로 나란히 풀면서 어디서 설계가 갈리는지 보여 주는 구간이다.
- `applied`는 기능을 하나씩 더 붙이는 단계라기보다, 운영 규약과 통합도, 제출용 표면을 키워 가는 구간이다.

## 이번 리라이트에서 지킨 원칙

- 기존 blog 초안은 입력으로 쓰지 않았다.
- 각 프로젝트는 `_evidence-ledger.md`, `_structure-plan.md`, `00-series-map.md`, `10-development-timeline.md` 네 문서로 유지했다.
- 코드 스니펫, 테스트 숫자, CLI 출력, 실패 메시지는 실제 확인한 근거를 기준으로 다시 정리했다.
