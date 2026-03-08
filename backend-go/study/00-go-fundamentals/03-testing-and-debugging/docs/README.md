# Docs

## Overview

이 과제는 table-driven test, subtest, benchmark, race-safe 자료구조를
작은 로그 분석 예제로 묶는다. 입문자가 “테스트를 쓰는 법”과 “테스트로 병목과
경합을 드러내는 법”을 같이 보는 데 목적이 있다.

## Concept Map

- 핵심 개념: [core-concepts.md](concepts/core-concepts.md)
- 참고 자료: [references/README.md](references/README.md)
- 검증 기록: [verification.md](verification.md)

## Why This Project

로그 파싱 예제는 입력 오류, 성능, 동시성 문제를 동시에 넣기 쉽다. 그래서
단위 테스트, benchmark, race detector를 한 번에 묶기 좋다.

