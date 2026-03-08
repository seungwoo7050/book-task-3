
# Legacy Inventory

## 실제 구성

- `legacy/Programming-Assignments`: 7개 Python 기반 구현 과제
- `legacy/Wireshark-Labs`: 7개 패킷 분석 랩
- `legacy/docs`: 온보딩과 실행 가이드 문서 모음

## 관찰된 노이즈

- `__pycache__/`, `.pytest_cache/`, `*.pyc` 같은 실행 부산물
- `web-proxy/problem/cache/*.dat` 같은 생성 캐시
- 일부 테스트는 `pytest` 단독 실행보다 `problem/Makefile test`를 전제로 설계됨

## 해석

레거시 트리는 자료 자체는 충분하지만, 문제 자료와 사용자 구현, 공개 인덱스, 개인 작업 로그가 한데 섞여 있어 학습 아카이브로 읽기에는 경계가 약했습니다. `study/`는 이 경계를 명확히 하기 위해 별도 트리로 재구성합니다.
