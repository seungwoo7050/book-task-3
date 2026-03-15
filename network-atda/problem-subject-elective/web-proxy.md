# web-proxy 문제지

## 왜 중요한가

이 문서는 Web Proxy를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 요청 전달: 프록시가 원 서버로 요청을 정확히 전달합니다, 응답 중계: 클라이언트가 원 서버 응답을 완전하게 받습니다, 캐시 재사용: 반복 요청을 캐시에서 처리합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-Application-Protocols-and-Sockets/web-proxy/problem/code/proxy_skeleton.py`
- `../study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`
- `../study/01-Application-Protocols-and-Sockets/web-proxy/problem/script/test_proxy.sh`
- `../study/01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py`
- `../study/01-Application-Protocols-and-Sockets/web-proxy/problem/Makefile`

## starter code / 입력 계약

- ../study/01-Application-Protocols-and-Sockets/web-proxy/problem/code/proxy_skeleton.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 요청 전달: 프록시가 원 서버로 요청을 정확히 전달합니다.
- 응답 중계: 클라이언트가 원 서버 응답을 완전하게 받습니다.
- 캐시 재사용: 반복 요청을 캐시에서 처리합니다.
- URL 파싱: 호스트, 포트, 경로를 올바르게 추출합니다.
- 동시성: 여러 연결을 처리할 수 있습니다.
- 코드 품질: 구조가 분명하고 읽기 쉬운 Python 코드입니다.

## 제외 범위

- `../study/01-Application-Protocols-and-Sockets/web-proxy/problem/code/proxy_skeleton.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/01-Application-Protocols-and-Sockets/web-proxy/problem/script/test_proxy.sh` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/01-Application-Protocols-and-Sockets/web-proxy/problem/code/proxy_skeleton.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `parse_url`와 `get_cache_path`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestURLParsing`와 `TestCachePath`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/01-Application-Protocols-and-Sockets/web-proxy/problem/script/test_proxy.sh` fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-proxy/problem test
```

- `web-proxy`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`web-proxy_answer.md`](web-proxy_answer.md)에서 확인한다.
