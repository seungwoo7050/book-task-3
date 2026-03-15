# 01 AWS Security Primitives structure outline

## 중심 질문

- 이 작은 엔진이 왜 이후 프로젝트들의 사소한 준비물이 아니라 판단 문법의 출발점인지
- allow/deny 결과보다 먼저 statement evidence와 precedence를 보여 주는 방식이 왜 중요한지

## 글 흐름

1. 문제 범위를 축소한 이유를 짚고 시작한다.
2. `Statement`/`Action`/`Resource` 정규화와 match reason 기록을 첫 축으로 둔다.
3. `explicit deny > allow > implicit deny`를 두 번째 축으로 둔다.
4. CLI JSON이 explainability를 외부 인터페이스로 고정하는 장면으로 닫는다.
5. 제외한 범위와 malformed input 가정을 마지막에 남긴다.

## 반드시 남길 증거

- `engine.py`의 `_as_list`, `_matches`, `Decision` return
- `cli.py`의 JSON 직렬화
- `test_engine.py`의 allow / deny override / no-match 세 시나리오
- `2026-03-14` CLI 재실행 결과
- `2026-03-14` pytest `3 passed in 0.01s`

## 반드시 피할 서술

- "IAM 엔진을 구현했다"는 식의 과장
- deny precedence를 개념 설명만 하고 테스트 근거를 빼먹는 서술
- explainability를 추상적 미덕으로만 적고 실제 `matches[]` shape를 숨기는 설명
- malformed input 방어가 이미 갖춰진 것처럼 보이게 만드는 문장

## 톤 체크

- 작은 프로젝트라도 단순 요약문이 아니라, 다음 프로젝트로 이어지는 판단 감각이 어떻게 생겼는지 chronology가 살아 있어야 한다.
- 홍보문보다 "무엇을 일부러 넣지 않았는지"까지 같이 읽히는 탐색형 톤을 유지한다.
