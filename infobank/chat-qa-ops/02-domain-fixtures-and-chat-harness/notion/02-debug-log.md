# 02-domain-fixtures-and-chat-harness 디버그 기록

## 검증 메모

- 테스트는 seeded KB 파일 집합과 첫 replay의 top-1 문서를 검증한다.
- DB나 vector store 없이도 회귀 입력 contract를 설명할 수 있어야 한다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: 짧은 한국어 질의가 content token만으로는 원하는 문서에 닿지 않을 수 있었다.
- 원인: 질의어와 문서 본문 단어가 완전히 일치하지 않아 filename 단서가 필요했다.
- 수정: 검색 점수에 doc_id 매칭도 포함해 fixture 재현성을 확보했다.
- 확인: `test_replay_harness_reproduces_expected_docs`가 `refund_policy.md`를 top-1로 요구한다.

## 재발 방지 체크리스트

- `python/data/knowledge_base/`
- `python/data/replay_sessions.json`
- `python/src/stage02/harness.py`
