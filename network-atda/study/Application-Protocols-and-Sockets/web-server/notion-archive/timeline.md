# Web Server — 개발 타임라인

## Phase 0: 환경 준비

```bash
# Python 3 확인 (표준 라이브러리만 사용하므로 별도 패키지 설치 없음)
python3 --version

# 프로젝트 디렉터리 구조 확인
# problem/code/       — skeleton 코드
# problem/data/       — 테스트용 hello.html
# problem/script/     — 검증 스크립트
# python/src/         — 솔루션 코드 작성 위치
# python/tests/       — pytest 테스트 파일
```

외부 패키지 설치가 필요 없다. `socket`, `threading`, `os`, `sys`는 모두 표준 라이브러리다.  
테스트 실행 시에만 `pytest`가 필요하다:

```bash
pip install pytest
```

## Phase 1: skeleton 분석 및 서버 소켓 기본 구조

**작업 파일**: `python/src/web_server.py`

1. `problem/code/server_skeleton.py`를 읽고 빈 칸을 파악했다
2. 서버 소켓 생성과 바인딩 구현:
   - `socket.socket(AF_INET, SOCK_STREAM)` — TCP 소켓 생성
   - `setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` — 재시작 시 포트 충돌 방지
   - `bind(("", port))` — 모든 인터페이스에서 수신
   - `listen(5)` — 백로그 큐 크기 5
3. accept 루프 구현 — `while True: accept()`

**CLI 확인**:
```bash
cd problem/data
python3 ../../python/src/web_server.py 6789
# 다른 터미널에서:
curl http://localhost:6789/
# → 이 시점에서는 연결만 되고 응답은 없음
```

## Phase 2: HTTP 요청 파싱

**작업 함수**: `handle_client(connection_socket, address)`

1. `connection_socket.recv(4096).decode()`로 요청 전문 수신
2. 첫 줄(`request_line`)을 `splitlines()[0]`으로 추출
3. `split()`으로 토큰 분리: `["GET", "/hello.html", "HTTP/1.1"]`
4. `tokens[1][1:]`로 경로에서 선행 `/` 제거 → `"hello.html"`
5. 빈 경로(`""`) 시 기본 파일 `"hello.html"` 지정

## Phase 3: 정적 파일 서빙 + 200 OK 응답

1. `open(filename, "rb")`로 바이너리 모드 읽기
2. `get_content_type()` 함수 작성 — 확장자별 MIME 타입 딕셔너리 매핑
3. HTTP 응답 헤더 조립:
   ```
   HTTP/1.1 200 OK\r\n
   Content-Type: text/html\r\n
   Content-Length: <바이트 수>\r\n
   Connection: close\r\n
   \r\n
   ```
4. `connection_socket.sendall(header.encode() + body)`로 헤더+본문 전송

**CLI 확인**:
```bash
cd problem/data
python3 ../../python/src/web_server.py 6789
# 다른 터미널:
curl -v http://localhost:6789/hello.html
# → 200 OK + HTML 본문 확인
```

## Phase 4: 404 Not Found 처리

1. `FileNotFoundError`를 `except`로 포착
2. 404 응답 헤더 + 에러 HTML 본문 조립
3. `NOT_FOUND_PAGE`를 모듈 레벨 상수로 정의
4. `Content-Length` 헤더에 에러 페이지 크기 명시

**CLI 확인**:
```bash
curl -v http://localhost:6789/does_not_exist.html
# → 404 Not Found 확인
```

## Phase 5: 멀티스레드 처리

1. `import threading`
2. `accept()` 후 `threading.Thread(target=handle_client, args=(...))` 생성
3. `t.daemon = True` 설정 — Ctrl+C 종료 시 스레드 자동 정리
4. `t.start()`로 비동기 시작

**CLI 확인**:
```bash
# 브라우저에서 http://localhost:6789/hello.html 열기
# → favicon.ico 등 병렬 요청이 동시 처리됨 확인
# → 서버 로그에 여러 [INFO] 라인이 거의 동시에 출력됨
```

## Phase 6: 예외 처리와 리소스 정리

1. `try/except/finally` 구조로 `handle_client` 전체 감싸기
2. `finally` 블록에서 `connection_socket.close()` 보장
3. 일반 `Exception`도 포착해 로그 출력 후 연결 닫기
4. `KeyboardInterrupt` 처리로 서버 종료 메시지 출력 후 `server_socket.close()`

## Phase 7: MIME 타입 확장

**작업 함수**: `get_content_type(filename)`

- `os.path.splitext()`로 확장자 추출
- 확장자-MIME 매핑 딕셔너리:
  `.html`, `.htm`, `.css`, `.js`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.ico`, `.txt`
- 미등록 확장자 → `application/octet-stream`

## Phase 8: 테스트 작성 및 검증

**작업 파일**: `python/tests/test_web_server.py`

1. `send_request()` 헬퍼: 소켓으로 직접 HTTP 요청 전송 후 상태 코드+본문 파싱
2. 테스트 케이스:
   - `test_200_ok_for_existing_file` — hello.html 요청 시 200
   - `test_response_contains_html` — 본문에 HTML 태그 포함
   - `test_404_for_missing_file` — 존재하지 않는 파일에 404
   - `test_404_body_contains_error_message` — 404 본문에 에러 메시지
   - `test_multiple_sequential_requests` — 연속 3회 요청 모두 200

**CLI 실행**:
```bash
# 터미널 1: 서버 시작
cd problem/data && python3 ../../python/src/web_server.py 6789

# 터미널 2: pytest 실행
cd python/tests && python3 -m pytest test_web_server.py -v
```

## Phase 9: Makefile 통합 검증

```bash
# 자동 검증 (서버 자동 기동 → 스크립트 실행 → 서버 종료)
make -C problem test
```

내부 동작:
1. `data/` 디렉터리에서 솔루션 서버를 백그라운드 기동
2. `script/test_server.sh`가 curl로 200/404 테스트 실행
3. `trap`으로 서버 프로세스 자동 종료

## 최종 파일 구조

```
web-server/
├── python/
│   ├── src/web_server.py          ← 솔루션 (160줄)
│   └── tests/test_web_server.py   ← pytest 테스트
├── problem/
│   ├── Makefile                   ← make test / make run-solution
│   ├── code/server_skeleton.py    ← 제공 skeleton
│   ├── data/hello.html            ← 테스트 HTML
│   └── script/test_server.sh      ← bash 검증 스크립트
├── docs/concepts/                 ← 개념 정리 노트
└── notion/                        ← 이 문서
```
