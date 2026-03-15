# Web Server Evidence Ledger

## 이번에 읽은 자료

- `problem/README.md`
- `python/src/web_server.py`
- `python/tests/test_web_server.py`

## 핵심 코드 근거

- `CONTENT_TYPES` map으로 MIME type 결정
- `handle_client()`에서 request line split 후 filename 추출
- `with open(filename, "rb")` 성공 시 `200 OK`
- `FileNotFoundError`에서 `404 Not Found`
- `main()` accept loop에서 connection마다 daemon thread 생성

## 테스트/검증 근거

`make -C network-atda/study/01-Application-Protocols-and-Sockets/web-server/problem test`

재실행 결과:

- existing file 200 pass
- missing file 404 pass
- body contains HTML pass

보조 단위 테스트는 sequential requests와 404 body까지 직접 확인한다.

## 이번에 남긴 해석

- 이 lab의 핵심은 웹 프레임워크가 아니라 파일 시스템과 socket 사이를 직접 잇는 것
- 현재 multi-threading은 "연결마다 새 thread" 수준이며, 확장성보다 구조 학습에 초점이 있다
