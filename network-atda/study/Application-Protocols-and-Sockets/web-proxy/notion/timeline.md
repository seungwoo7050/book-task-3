# Web Proxy — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
# 표준 라이브러리: socket, hashlib, os, sys, threading
# 테스트: pytest
pip install pytest
```

외부 패키지 없음. 테스트 스크립트에서 curl과 `python3 -m http.server`를 원 서버로 사용.

## Phase 1: skeleton 분석 및 서버 소켓

**작업 파일**: `python/src/web_proxy.py`

1. `problem/code/proxy_skeleton.py` 구조 파악
2. TCP 서버 소켓 생성/바인딩/리슨 — 웹 서버와 동일 패턴
3. `SO_REUSEADDR` 설정
4. 기본 포트 8888

**CLI 확인**:
```bash
python3 python/src/web_proxy.py 8888
# → [INFO] Proxy server started on port 8888
```

## Phase 2: URL 파싱 함수

**작업 함수**: `parse_url(url: str) -> tuple[str, int, str]`

1. `http://` 스킴 제거
2. 첫 `/` 기준으로 호스트부와 경로 분리
3. 호스트부에서 `:` 기준으로 호스트명과 포트 분리
4. 기본값: 포트 80, 경로 `/`

## Phase 3: 원 서버 연결 및 포워딩

**작업 함수**: `fetch_from_origin(hostname, port, path) -> bytes`

1. `socket.socket(AF_INET, SOCK_STREAM)` — 원 서버용 TCP 소켓
2. `settimeout(10)` — 10초 타임아웃
3. HTTP 요청 조립: `GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n`
4. `sendall()` 전송
5. 루프로 `recv(4096)` — 응답 전체 수신 (`chunk`가 빈 바이트일 때 종료)
6. 소켓 close

**CLI 확인**:
```bash
python3 python/src/web_proxy.py 8888
# 다른 터미널:
curl -x http://localhost:8888 http://www.example.com/
# → HTML 응답 출력
```

## Phase 4: 요청 파싱 및 라우팅

**작업 함수**: `handle_client(client_socket, address)`

1. `client_socket.recv(4096)` — 클라이언트 요청 수신
2. 첫 줄 파싱: `split()`으로 메서드, URL, 버전 추출
3. `GET`이 아니면 400 Bad Request 반환
4. `parse_url(url)`로 호스트/포트/경로 분리
5. `fetch_from_origin()`으로 원 서버 응답 획득
6. `client_socket.sendall(response)` — 클라이언트에 전달

## Phase 5: 캐시 구현

**작업 함수**: `get_cache_path(url: str) -> str`

1. `hashlib.md5(url.encode()).hexdigest()` — URL의 MD5 해시
2. `cache/{hash}.dat` 경로 반환
3. `os.makedirs(CACHE_DIR, exist_ok=True)` — cache 디렉터리 자동 생성

**캐시 로직 (handle_client 내)**:
1. 요청 URL로 캐시 경로 확인
2. 캐시 파일 존재 → 파일 읽어서 바로 반환 (원 서버 연결 안 함)
3. 캐시 미스 → 원 서버 fetch → 파일에 저장 → 클라이언트에 전달

**CLI 확인**:
```bash
# 첫 번째 요청 → [FETCH] + [CACHE] 로그
curl -x http://localhost:8888 http://www.example.com/

# 두 번째 요청 → [HIT] 로그
curl -x http://localhost:8888 http://www.example.com/

# 캐시 확인
ls cache/
```

## Phase 6: 에러 처리

1. `socket.timeout` → 504 Gateway Timeout
2. `socket.gaierror` (DNS 실패) → 502 Bad Gateway
3. `ConnectionRefusedError` → 502 Bad Gateway
4. 일반 `Exception` → 로그 출력 후 연결 닫기
5. `finally: client_socket.close()` — 항상 클라이언트 소켓 정리

## Phase 7: 멀티스레딩

```python
t = threading.Thread(target=handle_client, args=(client_socket, address))
t.daemon = True
t.start()
```

`listen(10)` — 웹 서버보다 큰 백로그 (여러 브라우저 탭 동시 사용 대비)

## Phase 8: 테스트

**작업 파일**: `python/tests/test_web_proxy.py`

```bash
# 터미널 1: 프록시 시작
python3 python/src/web_proxy.py 8888

# 터미널 2: curl로 직접 테스트
curl -x http://localhost:8888 http://www.example.com/
curl -x http://localhost:8888 http://www.example.com/  # 캐시 히트

# 테스트 스크립트: 원 서버 자동 기동 포함
make -C problem test
```

**test_proxy.sh 내부 동작**:
1. 임시 디렉터리에 `index.html` 생성
2. `python3 -m http.server 18080`으로 로컬 원 서버 기동
3. 프록시 통해 요청 → 200 확인
4. 원 서버 종료 후 같은 요청 → 캐시에서 200 확인

## Phase 9: 정리

```bash
make -C problem clean
# → cache/ 디렉터리 삭제, __pycache__ 정리
```

## 최종 파일 구조

```
web-proxy/
├── python/
│   ├── src/web_proxy.py           ← 솔루션 (220줄)
│   └── tests/test_web_proxy.py    ← pytest 테스트
├── problem/
│   ├── Makefile                   ← make test / make run-solution / make clean
│   ├── code/proxy_skeleton.py     ← 제공 skeleton
│   └── script/test_proxy.sh       ← 통합 검증 (원 서버 자동 기동)
├── docs/concepts/
└── notion/                        ← 이 문서
```
