# Web Server — 소켓 하나로 HTTP를 말하다

## 왜 이 과제부터 시작했나

네트워크 프로그래밍을 처음 접할 때 가장 자연스러운 출발점은 "브라우저에 URL을 치면 무슨 일이 일어나는가"였다. 교과서에서 TCP 3-way handshake, HTTP 요청-응답 모델을 읽었지만, 실제로 소켓을 열고 바이트를 주고받아 본 적은 없었다. 그래서 가장 단순한 HTTP 서버를 직접 만들어 보는 것을 첫 번째 과제로 골랐다.

목표는 명확했다. `python3 web_server.py`를 실행하면 브라우저에서 `http://localhost:6789/hello.html`을 열어 HTML 페이지가 뜨는 것. `http.server` 같은 표준 라이브러리의 고수준 모듈은 쓸 수 없고, 오직 `socket`과 `threading`만으로 구현해야 했다.

## 처음 마주한 것: TCP 소켓 수명주기

서버를 만들려면 소켓 하나가 어떤 일생을 사는지 먼저 이해해야 했다. `socket()` → `bind()` → `listen()` → `accept()` → `recv()`/`sendall()` → `close()`. 이 여섯 단계가 교과서에서 말하는 TCP 서버 소켓의 전부였다.

처음엔 이걸 그대로 순서대로 쓰면 될 줄 알았다. 실제로 `accept()`를 호출하면 클라이언트가 접속할 때까지 블로킹되고, 접속하면 새로운 소켓이 반환된다. 이 소켓으로 `recv()`를 호출해 HTTP 요청을 읽고, 파일을 열어서 `sendall()`로 보내면 된다.

문제는 **한 번에 하나의 클라이언트만 처리할 수 있다**는 점이었다. 브라우저는 보통 한 페이지를 열 때 여러 요청을 동시에 보낸다. favicon.ico, CSS, JS 등을 동시에 요청하는데, 서버가 첫 번째 요청을 처리하는 동안 나머지는 대기열에 갇혀버렸다.

## 멀티스레딩으로 동시 요청 처리

해결 방법은 `threading` 모듈이었다. `accept()`로 새 연결을 받을 때마다 별도의 스레드를 생성해서 `handle_client()` 함수에 넘기는 구조다.

```python
t = threading.Thread(target=handle_client, args=(connection_socket, address))
t.daemon = True
t.start()
```

여기서 `daemon = True`가 중요했다. 이걸 설정하지 않으면 Ctrl+C로 서버를 종료해도 활성 스레드가 남아서 프로세스가 죽지 않는다. 데몬 스레드로 만들면 메인 스레드가 종료될 때 함께 정리된다.

한 가지 알게 된 것은, 이 구조가 실제 프로덕션에서는 위험하다는 사실이다. 클라이언트 하나당 스레드 하나를 만들면, 동시 접속이 수천 개가 되면 스레드가 수천 개 생긴다. 하지만 이 과제의 범위에서는 "동시 요청이 되기는 한다"를 확인하는 것만으로 충분했다.

## HTTP 요청 파싱: 생각보다 단순한 규칙

브라우저가 보내는 HTTP 요청의 첫 줄은 이런 형태다:

```
GET /hello.html HTTP/1.1\r\n
```

이걸 파싱하는 건 `split()`만으로 가능했다. 첫 줄을 공백으로 쪼개면 `["GET", "/hello.html", "HTTP/1.1"]`. 두 번째 토큰에서 앞의 `/`를 떼면 파일명이 된다.

처음에는 이게 끝인 줄 알았다. 그런데 브라우저가 `http://localhost:6789/`만 입력하면 경로가 `/`만 온다. 빈 파일명을 어떻게 처리할지 결정해야 했고, `hello.html`을 기본 페이지로 설정했다.

## 파일 서빙과 Content-Type

파일을 읽어 보내는 것 자체는 `open(filename, "rb")`로 바이너리 모드로 열고 `f.read()`로 읽으면 끝이었다. 까다로운 부분은 **Content-Type 헤더**였다.

HTML 파일을 보내면서 `Content-Type: application/octet-stream`으로 보내면, 브라우저가 파일을 다운로드하려 든다. `.html` → `text/html`, `.css` → `text/css`, `.png` → `image/png` 같은 매핑이 필요했다.

이 매핑을 딕셔너리로 만들어두었다:

```python
CONTENT_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ...
}
```

`os.path.splitext()`로 확장자를 뽑고, 딕셔너리에 없으면 `application/octet-stream`을 기본값으로 쓰도록 했다.

## 404 응답 처리

존재하지 않는 파일을 요청하면 `FileNotFoundError`가 발생한다. 이걸 `try/except`로 잡아서 404 응답을 만들어 보냈다.

처음에는 단순히 연결을 끊어버릴까 생각했지만, HTTP 프로토콜에서 서버는 항상 응답을 보내야 한다. 응답 없이 연결을 끊으면 브라우저는 "연결이 재설정됨" 에러를 표시하는데, 이건 네트워크 장애인지 파일이 없는 건지 구분이 안 된다.

```
HTTP/1.1 404 Not Found\r\n
Content-Type: text/html\r\n
Content-Length: ...\r\n
\r\n
<html><body><h1>404 Not Found</h1></body></html>
```

이렇게 명시적으로 "없다"고 알려줘야 클라이언트가 상황을 구분할 수 있다.

## Connection: close와 리소스 정리

HTTP/1.1의 기본 동작은 keep-alive다. 즉, 하나의 연결로 여러 요청을 보낼 수 있다. 하지만 이 과제에서 keep-alive를 구현하려면 요청 경계를 정확히 파싱해야 하고, 복잡도가 급격히 올라간다.

그래서 모든 응답에 `Connection: close`를 붙였다. 한 번 응답을 보내면 연결을 닫는다는 뜻이다. 브라우저는 다음 요청을 위해 새 연결을 열게 되고, 서버 입장에서는 각 요청이 완전히 독립적으로 처리된다.

`finally` 블록에서 `connection_socket.close()`를 호출하는 것도 중요했다. 예외가 발생하든 안 하든 소켓은 반드시 닫아야 한다. 안 그러면 파일 디스크립터가 누수되어 결국 `Too many open files` 에러가 난다.

## SO_REUSEADDR: 사소하지만 중요한 옵션

서버를 Ctrl+C로 종료한 뒤 곧바로 다시 실행하면 `Address already in use` 에러가 나곤 했다. TCP 소켓은 종료 후에도 일정 시간 TIME_WAIT 상태로 남기 때문이다.

```python
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

이 한 줄을 `bind()` 전에 넣으면, 이전 소켓이 TIME_WAIT 상태에 있어도 같은 포트를 바인딩할 수 있다. 개발 중에는 서버를 수시로 재시작하니, 이 옵션이 없으면 매번 수십 초를 기다려야 한다.

## 테스트로 검증하기

구현이 끝난 뒤에는 두 가지 방법으로 검증했다.

먼저 `curl`로 직접 요청을 보내봤다:
```bash
curl -v http://localhost:6789/hello.html
```
200 응답과 함께 HTML 내용이 돌아오면 성공이다.

존재하지 않는 파일도 확인했다:
```bash
curl -v http://localhost:6789/nonexistent.html
```
404 응답이 돌아와야 한다.

자동화된 테스트는 `pytest`로 작성했다. 서버를 띄운 상태에서 소켓으로 직접 HTTP 요청을 보내고, 상태 코드와 본문을 검사하는 방식이다. 200/404 응답, 연속 요청 처리 등을 확인한다.

```bash
cd problem && make test
```

## 이 과제에서 가져간 것

파이썬 `socket` 모듈 하나로 브라우저와 대화할 수 있다는 점이 인상적이었다. HTTP라는 프로토콜이 바이트 스트림 위의 텍스트 규약일 뿐이라는 걸 직접 체감했다.

동시에, 이 구현이 "실제 서버"와 얼마나 먼지도 느꼈다. path traversal(`../../etc/passwd`)에 대한 방어가 없고, 무제한 스레드 생성이 가능하며, GET 이외의 메서드는 무시한다. 이런 한계를 인지한 채로 다음 과제(웹 프록시)로 넘어갔다.

---

> **학습 키워드**: TCP 소켓 수명주기, accept loop, HTTP 요청 파싱, Content-Type, 404 응답, threading, SO_REUSEADDR, `Connection: close`