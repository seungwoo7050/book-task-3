# Proxy Lab

## 이 프로젝트가 가르치는 것

`proxylab`은 HTTP 요청 파싱, header 정규화, concurrent connection 처리, in-memory cache 설계를 한 프로젝트 안에서 연결해 줍니다.
네트워크 I/O와 동시성 문제가 어떻게 서로 엮이는지 직접 확인하기 좋은 과제입니다.

## 누구를 위한 문서인가

- 소켓 프로그래밍을 단일 요청 처리에서 멈추지 않고 프록시 수준으로 확장해 보고 싶은 학습자
- thread-safe cache를 테스트 가능한 형태로 정리하고 싶은 사람
- 네트워크 과제를 포트폴리오용 저장소 구조로 정리하고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`c/README.md`](c/README.md)
3. [`cpp/README.md`](cpp/README.md)
4. [`docs/README.md`](docs/README.md)
5. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
proxylab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
  tests/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

문제 경계 확인:

```bash
cd problem
make clean && make
```

C 구현 검증:

```bash
cd c
make clean && make test
```

C++ 구현 검증:

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- 공개 문서는 HTTP forwarding, concurrency hazard, cache design을 설명합니다.
- 이 프로젝트는 외부 비공개 자산이 없으므로 테스트 하네스와 origin server까지 공개합니다.
- README는 구현 원리와 검증 흐름 중심으로 유지하고, 긴 실험 기록은 `notion/`으로 보냅니다.

## 포트폴리오로 확장하는 힌트

- 이 프로젝트는 네트워크와 동시성을 동시에 다뤘다는 점이 포트폴리오 강점입니다.
- 개인 저장소에서는 request/response 흐름도와 cache hit 예시를 추가하면 읽는 사람이 빠르게 이해할 수 있습니다.
