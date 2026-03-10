# Systems-Programming

## 이 트랙이 가르치는 것

이 트랙은 프로세스 제어, 시그널, 동적 메모리 관리, 네트워크 프록시를 실제 코드로 익히는 구간입니다.
CS:APP 후반부를 "운영체제와 시스템 프로그래밍 감각"으로 연결하는 역할을 합니다.

## 누구를 위한 문서인가

- 셸, 메모리 할당기, 프록시를 직접 구현해 보고 싶은 학습자
- 시스템 프로그래밍 과제를 공개 저장소에 정리하는 방법이 필요한 사람
- 동시성, 시그널, 캐시, 테스트 하네스 설계를 함께 보고 싶은 사람

## 먼저 읽을 곳

1. [`shlab/README.md`](shlab/README.md)
2. [`malloclab/README.md`](malloclab/README.md)
3. [`proxylab/README.md`](proxylab/README.md)

## 디렉터리 구조

```text
Systems-Programming/
  README.md
  shlab/
  malloclab/
  proxylab/
```

권장 순서는 `shlab -> malloclab -> proxylab`입니다.
프로세스와 시그널 감각을 먼저 익힌 뒤, 메모리와 네트워크로 확장하는 흐름을 전제로 합니다.

## 검증 방법

2026-03-10 문서 정비 기준으로 모든 프로젝트가 공개 구현용 테스트 경로를 갖고 있습니다.

- `shlab`: 직접 작성한 트레이스와 시그널 중심 테스트
- `malloclab`: 자체 trace driver 기반 정합성 검증
- `proxylab`: 로컬 origin server 기반 기능/동시성/캐시 테스트

구체 명령은 프로젝트별 `c/README.md`, `cpp/README.md`, `problem/README.md`를 따르면 됩니다.

## 스포일러 경계

- 이 트랙은 외부 비공개 바이너리를 다루지 않으므로 구현 원리와 테스트 전략을 비교적 넓게 공개합니다.
- 대신 README는 여전히 "학습 안내문" 역할에 집중하고, 긴 구현 해설은 `docs/`와 `notion/`으로 나눕니다.

## 포트폴리오로 확장하는 힌트

- 이 트랙은 코드 품질, 테스트 설계, 동시성 사고를 보여 주기 좋아 포트폴리오 가치가 높습니다.
- 개인 저장소에서는 각 프로젝트에 "실패했던 버그 한 가지"와 "검증 자동화 한 가지"를 강조하면 차별화가 큽니다.
