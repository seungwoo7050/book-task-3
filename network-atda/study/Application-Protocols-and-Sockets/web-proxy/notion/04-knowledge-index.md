# 04 지식 인덱스

## 핵심 용어
- **absolute URL**: 프록시가 받는 `http://host/path` 형태의 전체 URL이다.
- **origin-form**: 원본 서버가 기대하는 `/path?query` 형태의 요청 대상이다.
- **`502 Bad Gateway`**: 프록시가 원본 서버와 정상 연결을 못 했을 때 쓰는 대표 상태 코드다.
- **cache key**: 같은 자원을 다시 요청했는지 판단하는 기준 값이다.

## 다시 볼 파일
- [`../python/src/web_proxy.py`](../python/src/web_proxy.py): URL 파싱, 포워딩, 캐시 저장이 한 흐름으로 이어져 있다.
- [`../python/tests/test_web_proxy.py`](../python/tests/test_web_proxy.py): URL 파싱과 캐시 키가 어떤 입력에서 검증되는지 보여준다.
- [`../problem/script/test_proxy.sh`](../problem/script/test_proxy.sh): origin 서버 종료 후 캐시 히트를 확인하는 핵심 통합 검증 스크립트다.
- [`../docs/concepts/url-parsing.md`](../docs/concepts/url-parsing.md): 프록시에서 URL 분해가 왜 중요한지 요약한 문서다.

## 자주 쓰는 확인 명령
- `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test`
- `cd study/Application-Protocols-and-Sockets/web-proxy/python/tests && python3 -m pytest test_web_proxy.py -v`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음
