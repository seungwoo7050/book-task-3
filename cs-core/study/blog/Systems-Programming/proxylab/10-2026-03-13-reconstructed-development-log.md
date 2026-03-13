# Proxy Lab 재구성 개발 로그

`proxylab`은 HTTP 요청 파싱, header 정규화, concurrent connection 처리, in-memory cache 설계를 하나의 프록시 구현으로 묶는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

HTTP parsing, request rewriting, concurrent serve, cache promotion이 한 파일에서 어떻게 나뉘는지 순서대로 풀어낸다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: URI 파싱과 upstream request 조립을 먼저 세운다 — `c/src/proxy.c`
- Phase 2: 동시성 처리와 LRU cache를 serve path에 붙인다 — `c/src/proxy.c`
- Phase 3: origin server 기반 end-to-end test로 닫는다 — `tests/run_proxy_tests.sh`, `tests/origin_server.py`

## Phase 1. URI 파싱과 upstream request 조립을 먼저 세운다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 프록시의 첫 번째 일은 캐시가 아니라 올바른 요청을 origin으로 다시 보내는 일이다.

처음에는 header 정규화 전에 `parse_uri`와 `build_request`가 흔들리면 네트워크 디버깅이 전부 흐려질 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 URI 파싱, header append helper, canonical request builder를 먼저 묶어 upstream surface를 고정했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/proxy.c`
- CLI: `make clean && make test`
- 검증 신호: request builder가 먼저 고정돼 있어 이후 캐시/동시성 문제를 분리해서 볼 수 있다.

### 이 장면을 고정하는 코드 — `parse_uri` (`c/src/proxy.c:156`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```c
static int parse_uri(const char *uri, char *host, char *port, char *path)
{
    const char *host_start = uri;
    const char *path_start;
    const char *colon;
    size_t host_len;
```

`Parse_Uri`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 네트워크 프로그램도 초기 단계는 소켓보다 문자열 계약을 얼마나 안정적으로 다루는지가 더 중요했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 concurrent serve와 cache path로 넘어간다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 네트워크 프로그램도 초기 단계는 소켓보다 문자열 계약을 얼마나 안정적으로 다루는지가 더 중요했다.

그래서 다음 장면에서는 concurrent serve와 cache path로 넘어간다.

## Phase 2. 동시성 처리와 LRU cache를 serve path에 붙인다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `handle_client`, `cache_lookup`, `cache_store`, `promote_entry`가 실제 프록시의 중간 설계 축이다.

처음에는 멀티클라이언트 처리를 붙이는 순간 캐시 일관성과 request forwarding이 함께 흔들릴 거라고 예상했다. 그런데 실제로 글의 중심이 된 조치는 client handler에서 forwarding과 caching을 한 번에 다루되, cache list 조작은 helper로 분리해 LRU 이동을 명확히 했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/proxy.c`
- CLI: `make clean && make test`
- 검증 신호: cache helper 분리가 있어야 동시성과 캐시 논의를 같은 파일 안에서도 추적할 수 있다.

### 이 장면을 고정하는 코드 — `handle_client` (`c/src/proxy.c:245`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```c
static void handle_client(int clientfd)
{
    char buf[MAXLINE];
    char method[MAXLINE];
    char uri[MAXLINE];
    char version[MAXLINE];
    char host[MAXLINE];
    char port[MAXLINE];
    char path[MAXLINE];
    char request[MAX_REQUEST_SIZE];
    char *cached_data = NULL;
    size_t cached_size = 0;
```

`Handle_Client`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 캐시는 성능 기능이 아니라 concurrent serve path를 깨뜨리지 않으면서 반복 요청을 흡수하는 별도 contract였다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 self-owned origin server로 전체 루프를 검증한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 캐시는 성능 기능이 아니라 concurrent serve path를 깨뜨리지 않으면서 반복 요청을 흡수하는 별도 contract였다.

그래서 다음 장면에서는 self-owned origin server로 전체 루프를 검증한다.

## Phase 3. origin server 기반 end-to-end test로 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 proxy는 unit-level helper만으로 끝나지 않고 실제 요청/응답 루프를 확인해야 한다.

처음에는 공식 driver 없이도 `tests/origin_server.py`와 shell harness가 있으면 구현 흐름을 충분히 재현할 수 있다고 판단했다. 그런데 실제로 글의 중심이 된 조치는 README와 Makefile을 `run_proxy_tests.sh` 중심으로 묶어 end-to-end 검증을 공개 표면에 올렸다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `tests/run_proxy_tests.sh`, `tests/origin_server.py`
- CLI: `make clean && make test`
- 검증 신호: origin fixture와 shell harness가 마지막 검증 신호를 남긴다.

### 이 장면을 고정하는 코드 — `Handler` (`tests/origin_server.py:14`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```python
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, format, *args):
        return
```

`Handler`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 네트워크 프로그램일수록 self-owned origin fixture가 reasoning을 재현하는 핵심 자산이 됐다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 request surface, concurrent handler, cache verification 순서로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 네트워크 프로그램일수록 self-owned origin fixture가 reasoning을 재현하는 핵심 자산이 됐다.

그래서 다음 장면에서는 request surface, concurrent handler, cache verification 순서로 닫는다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/c && make clean && make test)
```

```text
Proxy tests passed
bash ../tests/run_proxy_tests.sh ./build/proxy
```

## 이번에 남은 질문

- 개념 축: `concurrency and cache`, `http forwarding`
- 대표 테스트/fixture: `tests/origin_server.py`, `tests/run_proxy_tests.sh`
- 다음 질문: 최종 글은 request surface, concurrent handler, cache verification 순서로 닫는다.
