# 05 개발 타임라인

이 문서는 `Web Server`를 처음 읽는 학생이 가장 먼저 따라가야 하는 재현 가이드다. 이 프로젝트에서 한 파일만 읽는다면 이 문서부터 보고, 명령을 직접 실행한 뒤 나머지 노트를 읽는 것을 권장한다.

## 준비
- `python3`
- `curl`
- `pytest`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 문서를 열어 문제 경계부터 확인한다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/server_skeleton.py`](../problem/code/server_skeleton.py)
- [`../problem/data/hello.html`](../problem/data/hello.html)

여기서 확인할 질문은 세 가지면 충분하다.
- 어떤 요청만 처리하면 되는가
- 어떤 파일이 제공물이고 어떤 파일이 내 구현인가
- 검증은 어떤 명령으로 끝내는가

## 단계 2. 현재 구현을 짧게 훑기
바로 코드를 다 읽기보다 핵심 파일 두 개만 먼저 본다.
- [`../python/src/web_server.py`](../python/src/web_server.py)
- [`../python/tests/test_web_server.py`](../python/tests/test_web_server.py)

이 단계에서 확인할 포인트는 다음이다.
- 요청 라인을 어디서 파싱하는가
- `/` 요청을 어떻게 `hello.html`로 바꾸는가
- `404`와 `Content-Type`은 어떤 기준으로 결정되는가

## 단계 3. 자동 검증 먼저 실행
가장 먼저 아래 명령으로 현재 상태를 고정한다.

```bash
make -C study/01-Application-Protocols-and-Sockets/web-server/problem test
```

기대 결과:
- 테스트 스크립트가 오류 없이 종료된다.
- `200 OK`, `404 Not Found`, HTML 본문, 순차 요청 검증이 함께 통과한다.

자동 검증 범위를 더 세밀하게 보고 싶다면 아래도 바로 실행한다.

```bash
cd study/01-Application-Protocols-and-Sockets/web-server/python/tests
python3 -m pytest test_web_server.py -v
```

## 단계 4. 수동으로 동작을 다시 본다
터미널 1:

```bash
make -C study/01-Application-Protocols-and-Sockets/web-server/problem run-solution
```

터미널 2:

```bash
curl -i http://localhost:6789/hello.html
curl -i http://localhost:6789/
curl -i http://localhost:6789/missing.html
```

기대 결과:
- `hello.html` 요청과 `/` 요청은 `200 OK`가 나온다.
- `/` 요청은 실제로 `hello.html`을 돌려준다.
- 없는 파일은 `404 Not Found`와 오류 본문을 돌려준다.
- 응답 후 연결이 깔끔하게 닫힌다.

## 단계 5. 실패하면 가장 먼저 볼 곳
- 포트가 이미 사용 중이면 `SO_REUSEADDR`와 기존 서버 프로세스를 먼저 확인한다.
- 브라우저 렌더링이 이상하면 `Content-Type` 매핑을 먼저 본다.
- 응답이 끝나지 않으면 `Connection: close`와 소켓 종료 위치를 먼저 본다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 6. 완료 판정
아래 네 가지가 되면 이 프로젝트는 재현한 것으로 본다.
- 문제 범위와 제공물 경계를 설명할 수 있다.
- `make test`가 통과한다.
- `curl`로 `200`과 `404`를 직접 확인했다.
- [`01-approach-log.md`](01-approach-log.md)와 [`02-debug-log.md`](02-debug-log.md)를 읽고 왜 지금 구조가 되었는지 설명할 수 있다.
