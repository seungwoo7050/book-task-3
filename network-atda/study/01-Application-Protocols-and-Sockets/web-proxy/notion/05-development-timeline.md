# 05 개발 타임라인

이 문서는 `Web Proxy`를 처음 재현하는 학생을 위한 실행 가이드다. 핵심은 단순히 프록시가 중간에서 요청을 전달하는지 보는 데서 끝나지 않고, 캐시 hit를 결정적으로 증명하는 데 있다.

## 준비
- `python3`
- `curl`
- `pytest`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/proxy_skeleton.py`](../problem/code/proxy_skeleton.py)
- [`../problem/script/test_proxy.sh`](../problem/script/test_proxy.sh)

이 단계에서 확인할 질문:
- 프록시가 어떤 형식의 요청을 받는가
- 캐시 검증은 어떤 시나리오로 하는가
- 왜 외부 인터넷 대신 로컬 origin 서버 스크립트가 중요한가

## 단계 2. 구현과 자동 테스트 기준을 먼저 본다
- [`../python/src/web_proxy.py`](../python/src/web_proxy.py)
- [`../python/tests/test_web_proxy.py`](../python/tests/test_web_proxy.py)

여기서 확인할 포인트:
- URL 파싱 함수가 호스트, 포트, 경로를 어떻게 나누는가
- 캐시 파일명이 왜 URL 원문이 아니라 해시인지
- 어떤 URL 패턴이 공식 테스트 범위에 들어가는가

## 단계 3. 자동 검증 먼저 실행
아래 명령이 가장 안정적인 재현 시작점이다.

```bash
make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test
```

기대 결과:
- 임시 프록시가 뜬다.
- 로컬 origin 서버 대상 통합 검증이 통과한다.
- 캐시 저장과 cache hit가 스크립트로 확인된다.

세부 단위 검증은 아래로 확인한다.

```bash
cd study/01-Application-Protocols-and-Sockets/web-proxy/python/tests
python3 -m pytest test_web_proxy.py -v
```

## 단계 4. 수동으로 cache hit를 다시 만든다
터미널 1:

```bash
make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem run-solution
```

터미널 2:

```bash
bash study/01-Application-Protocols-and-Sockets/web-proxy/problem/script/test_proxy.sh 8888
```

기대 결과:
- 첫 요청은 origin 서버를 통해 응답한다.
- 캐시 파일이 생성된다.
- origin 서버가 내려간 뒤 같은 URL 요청이 cache hit로 통과한다.

외부 요청을 한 번 직접 보내 보고 싶다면 아래 명령을 추가로 써도 된다.

```bash
make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem request
```

## 단계 5. 실패하면 가장 먼저 볼 곳
- origin 서버가 요청을 이해하지 못하면 절대 URL을 origin-form으로 다시 쓰는지 먼저 확인한다.
- 캐시 파일 생성이 이상하면 해시 키와 `cache/` 디렉터리를 본다.
- 에러 코드가 모호하면 `502`와 `504` 분기 위치를 확인한다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 6. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- `make test`가 통과한다.
- 로컬 스크립트로 cache hit를 직접 확인했다.
- URL 파싱 테스트와 캐시 키 테스트가 왜 필요한지 설명할 수 있다.
- 프록시가 서버이면서 동시에 클라이언트라는 점을 말할 수 있다.
