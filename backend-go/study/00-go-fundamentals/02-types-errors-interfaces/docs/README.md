# Docs

## Overview

이 과제는 Go의 struct, method, interface, custom error를 한 번에 다룬다.
입문자가 “값을 담는 타입”, “행동을 추상화하는 인터페이스”, “의미 있는 에러”를
처음 분리해 보는 지점이다.

## Concept Map

- 핵심 개념: [core-concepts.md](concepts/core-concepts.md)
- 참고 자료: [references/README.md](references/README.md)
- 검증 기록: [verification.md](verification.md)

## Why This Project

`Catalog` 예제는 입문자가 interface를 과하게 추상화하지 않고도 실용적인 용도를
보게 해 준다. 동시에 `errors.As`, sentinel error, pointer receiver를 익히기에
문제 크기가 적당하다.

