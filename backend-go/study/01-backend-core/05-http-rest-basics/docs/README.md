# Docs

## Overview

이 과제는 REST API의 가장 작은 핵심인 method, status code, JSON I/O,
validation, pagination, idempotency key의 의미를 묶어서 익히도록 설계했다.

## Concept Map

- 핵심 개념: [core-concepts.md](concepts/core-concepts.md)
- 참고 자료: [references/README.md](references/README.md)
- 검증 기록: [verification.md](verification.md)

## Why This Project

`go-api-standard`보다 작은 문제에서 HTTP 감각을 먼저 잡아 두면 이후 과제의
설계 의도를 훨씬 빠르게 읽을 수 있다. 특히 `401/403`, `201/200`, validation
오류 처리 같은 기본 감각을 초반에 고정하는 데 도움이 된다.

