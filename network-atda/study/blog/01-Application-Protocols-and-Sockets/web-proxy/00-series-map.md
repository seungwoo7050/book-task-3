# Web Proxy series map

이 프로젝트를 읽을 때 붙들 질문은 하나다. 클라이언트 요청, origin fetch, cache 저장을 프록시 안에서 어떻게 이어 붙였는가?

## 무엇을 근거로 복원했는가

- 프로젝트 README: `study/01-Application-Protocols-and-Sockets/web-proxy/README.md`
- 문제 문서와 실행 표면: `study/01-Application-Protocols-and-Sockets/web-proxy/problem/README.md`, `study/01-Application-Protocols-and-Sockets/web-proxy/problem/Makefile`
- 핵심 구현과 테스트: `study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`, `study/01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py`
- 정식 검증 출력: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`

## 어떤 순서로 읽으면 되는가

1. `problem/README.md`로 문제 조건과 성공 기준을 확인한다.
2. 이 문서에서 어떤 입력을 근거로 썼는지 먼저 본다.
3. `01-evidence-ledger.md`로 세 단계 흐름을 짧게 파악한다.
4. `10-development-timeline.md`에서 코드나 trace, CLI를 따라간다.

## 이번 리라이트에서 의도적으로 제외한 입력

- 현재 `study/blog/**`의 이전 본문
- `notion/`, `notion-archive/` 아래의 서술형 메모

## 짧은 판정 메모

- 독립 프로젝트로 본 이유: `Web Proxy`는 자기 README와 정식 검증 명령으로 범위를 독립적으로 설명할 수 있다.
- 보관본 위치: `study/blog/_legacy`
- 이번 글의 중심 답: 클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.
