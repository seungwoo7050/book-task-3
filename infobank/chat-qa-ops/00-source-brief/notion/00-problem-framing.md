# 00-source-brief 문제 정의

## 이 stage가 푸는 문제

legacy 감사 결과와 최종 capstone 방향을 실행 가능한 source brief contract로 고정하는 단계다.

## 성공 기준

- 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다.
- reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다.
- 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다.

## 왜 지금 이 단계를 먼저 보는가

- `08/v0`를 기준점으로 삼는 이유를 stage 단위에서 먼저 고정한다.
- 이후 모든 README와 verification 문서는 이 source brief를 따라야 한다.

## 먼저 알고 있으면 좋은 것

- 루트 문서에서 legacy intent와 새 커리큘럼 순서를 읽어야 한다.
- capstone이 챗봇 제품이 아니라 QA Ops 플랫폼이라는 점을 먼저 이해해야 한다.

## 확인할 증거

- `python/tests/test_source_brief.py`가 baseline version과 stack contract를 검증한다.
- 생성된 stage README가 `00 -> 08` 순서를 repository-level index로 연결한다.

## 아직 남아 있는 불확실성

이 단계는 설계 방향을 고정할 뿐, 실제 evaluator나 dashboard가 동작함을 입증하지는 않는다.
