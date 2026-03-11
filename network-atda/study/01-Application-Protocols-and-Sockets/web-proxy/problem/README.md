# Web Proxy 문제 안내

## 이 문서의 역할

이 문서는 `Web Proxy`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

클라이언트의 HTTP GET 요청을 원 서버로 전달하고, 응답을 다시 클라이언트에 돌려주며, 같은 URL에 대해서는 캐시를 재사용하는 프록시 서버를 구현합니다.

## 구현해야 할 동작

### 프록시 서버 수신

- 기본 포트 `8888`(변경 가능)에서 TCP 연결을 받습니다.
- 클라이언트 연결을 accept해 요청을 읽습니다.

### 요청 파싱

- 프록시 요청에 포함된 절대 URL을 파싱합니다.
- 호스트 이름, 포트(기본 80), 경로를 추출합니다.

### 원 서버로 전달

- 원 서버에 TCP 연결을 열고 상대 경로 기반 HTTP 요청으로 바꿔 전달합니다.
- `Host` 헤더와 `Connection: close`를 적절히 포함합니다.

### 응답 중계

- 원 서버 응답 전체를 읽어 클라이언트에 그대로 전달합니다.
- 전송 후 연결을 닫습니다.

### 캐시

- 새 응답은 로컬에 저장합니다.
- 같은 URL 요청이 다시 오면 원 서버에 가지 않고 캐시를 반환합니다.
- URL 해시를 캐시 파일 이름으로 사용할 수 있습니다.

### 동시성

- 클라이언트 연결마다 별도 스레드로 처리합니다.

## 제공 자료와 실행 환경

- starter code: `code/proxy_skeleton.py`
- 검증 스크립트: `script/test_proxy.sh`
- 수동 확인 예시: `curl -x http://localhost:8888 http://www.example.com/`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- `http.client`, `urllib`, `requests` 같은 HTTP 라이브러리는 사용하지 않습니다.
- 범위는 HTTP GET으로 제한하고 `HTTPS CONNECT`는 다루지 않습니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 요청 전달 | 프록시가 원 서버로 요청을 정확히 전달합니다. |
| 응답 중계 | 클라이언트가 원 서버 응답을 완전하게 받습니다. |
| 캐시 재사용 | 반복 요청을 캐시에서 처리합니다. |
| URL 파싱 | 호스트, 포트, 경로를 올바르게 추출합니다. |
| 동시성 | 여러 연결을 처리할 수 있습니다. |
| 코드 품질 | 구조가 분명하고 읽기 쉬운 Python 코드입니다. |

## 출력 예시

```text
[INFO] Proxy server started on port 8888
[FETCH] GET http://www.example.com/index.html -> origin server
[CACHE] Stored: cache/a1b2c3d4.dat
[HIT]   GET http://www.example.com/index.html -> served from cache
```
