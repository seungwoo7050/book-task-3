# Proxy Lab

`proxylab`은 HTTP 요청 파싱, header 정규화, concurrent connection 처리, in-memory cache 설계를 하나의 프록시 구현으로 묶는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| 단일 origin server 앞에서 동작하는 concurrent HTTP proxy와 캐시를 구현한다. | header 정규화, connection handling, thread-safe cache 계약을 함께 만족해야 하고, local origin server 기반 검증을 유지한다. | C 답은 [`c/src/proxy.c`](c/src/proxy.c), C++ 답은 [`cpp/src/proxy.cpp`](cpp/src/proxy.cpp), 공용 시나리오는 `tests/`와 `docs/`에 둔다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | socket I/O, HTTP forwarding, concurrent cache, 기능 테스트 설계 | `public verified` |

실제 소스코드·테스트·검증 엔트리 기준의 blog 시리즈: [`../../blog/Systems-Programming/proxylab/00-series-map.md`](../../blog/Systems-Programming/proxylab/00-series-map.md)

## 디렉터리 역할

- `problem/`: starter contract와 최소 빌드 경계
- `c/`, `cpp/`: proxy 구현과 구현별 테스트
- `tests/`: origin server와 캐시 시나리오 검증
- `docs/`: HTTP forwarding, concurrency hazard, cache 설계 정리
- `notion/`: 디버그 로그와 재검증 기록

## 검증 빠른 시작

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

## 공개 경계

- 공개 문서는 HTTP forwarding, concurrency hazard, cache design을 설명한다.
- 외부 비공개 자산이 없으므로 테스트 하네스와 origin server까지 공개한다.
- README는 구현 원리와 검증 흐름 중심으로 유지하고, 긴 실험 기록은 `notion/`으로 보낸다.
