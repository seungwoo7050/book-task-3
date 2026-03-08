# Docs

## Overview

이 과제는 legacy distributed log 과제에서 실제 구현된 핵심 범위만 남겨
`distributed-log-core`로 재정의한 것이다. store, index, segment, log 구조에
집중한다.

## Concept Map

- 핵심 개념: [core-concepts.md](concepts/core-concepts.md)
- 참고 자료: [references/README.md](references/README.md)
- 검증 기록: [verification.md](verification.md)

## Why This Project

append-only log 구조는 Kafka류 시스템을 이해하는 데 좋은 학습 재료지만,
replication까지 한 번에 넣으면 입문 난도가 너무 커진다. 그래서 core 범위만 유지했다.

