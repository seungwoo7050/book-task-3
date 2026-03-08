# Docs

## Overview

이 과제는 cache-aside, cache invalidation, structured logging, metrics,
trace header 전파를 한 프로젝트에 묶는다. CRUD 이후 “운영 감각”을 붙이는 단계다.

## Concept Map

- 핵심 개념: [core-concepts.md](concepts/core-concepts.md)
- 참고 자료: [references/README.md](references/README.md)
- 검증 기록: [verification.md](verification.md)

## Why This Project

입문자가 API와 DB만 배우면 실제 운영 문제를 너무 늦게 만나게 된다. 이 과제는
캐시 적중/미스, invalidation, metrics 노출 같은 운영 기초를 일찍 묶어 본다.

