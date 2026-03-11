# 00-source-brief 디버그 기록

## 검증 메모

- 테스트는 topic, baseline version, primary stack, reference spine 길이를 고정한다.
- runtime을 검증하는 단계는 아니므로 build보다 contract drift 방지가 핵심이다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: stack 설명이 문서마다 조금씩 달라질 위험이 있었다.
- 원인: Python 버전과 backend/frontend 주력 기술이 코드가 아니라 서술에만 있었다.
- 수정: SourceBrief에 Python 3.12, FastAPI, React, PostgreSQL, Langfuse를 명시하고 테스트로 고정했다.
- 확인: `python/tests/test_source_brief.py`가 stack membership와 baseline version을 검증한다.

## 재발 방지 체크리스트

- `python/src/stage00/source_brief.py`
- `python/tests/test_source_brief.py`
