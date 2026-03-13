# Systems-Programming 블로그 트랙

CSAPP 후반부 3개 시스템 프로그래밍 프로젝트의 개발 타임라인.
메모리 관리, 프로세스 제어, 네트워크 프록시를 다룬다.

## 프로젝트 목록

| 프로젝트 | 핵심 주제 | 시리즈 |
|----------|-----------|--------|
| [Malloc Lab](malloclab/) | 동적 메모리 할당기, free list, coalesce | [→](malloclab/00-series-map.md) |
| [Shell Lab](shlab/) | SIGCHLD/SIGINT/SIGTSTP, job table, sigsuspend | [→](shlab/00-series-map.md) |
| [Proxy Lab](proxylab/) | HTTP proxy, 멀티스레드, LRU 캐시 | [→](proxylab/00-series-map.md) |

## 공개 경계

- **공개**: C/C++ companion 코드, 검증 경로, 학습 로그
- **local-only**: 공식 mdriver traces, official binary
