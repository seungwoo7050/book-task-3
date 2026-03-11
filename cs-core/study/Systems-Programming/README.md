# Systems-Programming

`Systems-Programming`은 프로세스 제어, 시그널, 메모리 관리, 네트워크 프록시를 실제 구현으로 묶어 시스템 프로그래밍 계약을 익히는 트랙이다.

## 프로젝트 지도

| 프로젝트 | 문제 | 이 레포의 답 | 검증 시작점 | 상태 |
| --- | --- | --- | --- | --- |
| [`shlab`](shlab/README.md) | process group과 foreground/background job control shell 구현 | `c/src/tsh.c`, `cpp/src/tsh.cpp`, `tests/` | [`problem`](shlab/problem/README.md), [`c`](shlab/c/README.md), [`cpp`](shlab/cpp/README.md) | `public verified` |
| [`malloclab`](malloclab/README.md) | explicit free list allocator와 `realloc` 경계 구현 | `c/src/mm.c`, `cpp/src/mm.cpp`, `docs/` | [`problem`](malloclab/problem/README.md), [`c`](malloclab/c/README.md), [`cpp`](malloclab/cpp/README.md) | `public verified` |
| [`proxylab`](proxylab/README.md) | concurrent HTTP proxy와 in-memory cache 구현 | `c/src/proxy.c`, `cpp/src/proxy.cpp`, `tests/` | [`problem`](proxylab/problem/README.md), [`c`](proxylab/c/README.md), [`cpp`](proxylab/cpp/README.md) | `public verified` |

## 권장 순서

1. [`shlab`](shlab/README.md)
2. [`malloclab`](malloclab/README.md)
3. [`proxylab`](proxylab/README.md)

- `필수 코어`: `shlab -> malloclab`
- `심화/선택`: `proxylab`

## 검증 원칙

- `shlab`은 self-owned trace와 shell test로 process/signal 경계를 검증한다.
- `malloclab`은 starter contract 위에 작성한 allocator를 `c/`, `cpp/` 테스트로 검증한다.
- `proxylab`은 local origin server와 캐시 테스트를 포함한 공개 검증 경로를 유지한다.

## 공개 경계

- 이 트랙은 외부 비공개 바이너리에 의존하지 않으므로 구현 코드, 테스트 하네스, 개념 문서를 비교적 넓게 공개한다.
- README는 `문제`, `답`, `검증`만 짧게 안내하고, 긴 구현 reasoning은 각 프로젝트 `docs/`, `notion/`으로 보낸다.
- authored comment는 한국어를 기본으로 유지하되 protocol, system call, code identifier는 English 그대로 둔다.
