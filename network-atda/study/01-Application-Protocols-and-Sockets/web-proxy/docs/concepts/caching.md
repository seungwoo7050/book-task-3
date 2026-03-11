# 웹 캐싱 전략과 구현

## 개요

웹 캐싱(Web Caching)은 이전에 요청된 웹 리소스의 사본을 로컬에 저장하여, 동일한 리소스에 대한 후속 요청 시 원본 서버에 접촉하지 않고 즉시 응답하는 기술이다. 프록시 서버에서의 캐싱은 네트워크 성능 최적화의 핵심 요소다.

## 캐싱의 이점

| 이점 | 설명 |
| :--- | :--- |
| **지연 감소** | 원본 서버까지 왕복할 필요 없이 로컬에서 즉시 응답 |
| **대역폭 절감** | 동일 데이터를 반복 전송하지 않아 네트워크 트래픽 감소 |
| **서버 부하 경감** | 원본 서버의 요청 처리량 감소 |
| **가용성 향상** | 원본 서버가 일시적으로 다운되어도 캐시된 응답 제공 가능 |

> Kurose & Ross, *Computer Networking* — Chapter 2에서 웹 캐싱을 "조건부 GET"과 함께 HTTP의 핵심 성능 기법으로 설명한다.

## 캐시 동작 흐름

```
클라이언트 요청 도착
        │
        ▼
  ┌─────────────┐
  │ 캐시 조회    │
  │ (URL 해시)   │
  └──────┬──────┘
         │
    ┌────┴────┐
    ▼         ▼
  HIT       MISS
    │         │
    │    ┌────┴────┐
    │    │원본 서버 │
    │    │요청/응답 │
    │    └────┬────┘
    │         │
    │    캐시 저장
    │         │
    ▼         ▼
 클라이언트에 응답 전송
```

## 캐시 키 설계

### URL 해시 방식

이 과제에서는 URL의 MD5 해시를 캐시 파일명으로 사용한다:

```python
import hashlib
import os

CACHE_DIR = "cache"

def get_cache_path(url: str) -> str:
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.dat")
```

**장점**: 
- 파일명으로 안전한 고정 길이 문자열 생성
- URL에 특수문자(`/`, `?`, `&` 등)가 있어도 문제없음

**단점**:
- MD5 충돌 가능성 (실용적으로는 무시 가능)
- 해시만으로는 어떤 URL의 캐시인지 역추적 불가

### 대안: URL 인코딩 방식

```python
import urllib.parse
cache_key = urllib.parse.quote(url, safe="")
# "http://example.com/page" → "http%3A%2F%2Fexample.com%2Fpage"
```

이 방식은 가독성이 좋지만, URL이 길면 파일명도 길어지는 문제가 있다.

## 캐시 저장과 조회

### 저장 (Cache Store)

```python
def cache_store(url: str, response: bytes) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = get_cache_path(url)
    with open(path, "wb") as f:
        f.write(response)
```

### 조회 (Cache Lookup)

```python
def cache_lookup(url: str) -> bytes | None:
    path = get_cache_path(url)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None
```

## 캐시 무효화 (이 과제 범위 밖)

실제 HTTP 캐싱에서는 다양한 무효화 메커니즘이 존재한다:

### 1. TTL (Time-To-Live)

```
Cache-Control: max-age=3600
```

→ 캐시된 응답은 3600초(1시간) 동안 유효

### 2. 조건부 GET (Conditional GET)

```
GET /index.html HTTP/1.1
If-Modified-Since: Wed, 09 Apr 2025 08:38:00 GMT
```

→ 서버가 `304 Not Modified`로 응답하면 캐시 사용, 그렇지 않으면 새 응답으로 교체

### 3. ETag

```
ETag: "abc123"
If-None-Match: "abc123"
```

→ 서버의 리소스 변경 여부를 태그 비교로 확인

> 이 과제에서는 **단순 캐시**(무조건 저장, 만료 없음)만 구현한다. 프로덕션 환경에서는 반드시 무효화 정책이 필요하다.

## 멀티스레드 환경에서의 캐시 안전성

동시에 같은 URL을 요청하면 **레이스 컨디션**이 발생할 수 있다:

1. Thread A: 캐시 조회 → MISS
2. Thread B: 캐시 조회 → MISS  
3. Thread A: 원본 서버 요청, 캐시 저장
4. Thread B: 원본 서버 요청, 캐시 **덮어쓰기**

이 과제에서는 같은 응답을 덮어쓰므로 데이터 무결성 문제는 없지만, 불필요한 중복 요청이 발생한다.

**해결 방법 (고급)**:
```python
import threading

cache_locks = {}
global_lock = threading.Lock()

def get_or_fetch(url):
    with global_lock:
        if url not in cache_locks:
            cache_locks[url] = threading.Lock()
        lock = cache_locks[url]
    
    with lock:
        cached = cache_lookup(url)
        if cached:
            return cached
        response = fetch_from_origin(url)
        cache_store(url, response)
        return response
```

## 참고 자료

- [RFC 7234 — HTTP/1.1 Caching](https://www.rfc-editor.org/rfc/rfc7234)
- [MDN — HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- Kurose & Ross, *Computer Networking* — Chapter 2.2.5 (Web Caching)
