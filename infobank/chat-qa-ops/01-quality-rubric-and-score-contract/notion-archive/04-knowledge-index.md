# Quality Rubric — 지식 인덱스

## 핵심 개념

### Weighted Rubric 설계

상담 품질을 하나의 숫자로 압축하되, 어떤 축이 더 중요한지를 명시하는 방식이다.
이 프로젝트에서는 다섯 축을 사용한다:

- **Correctness (30%)**: 답변 내용이 사실에 부합하는가
- **Groundedness (25%)**: 답변이 참조할 수 있는 근거 문서에 기반하는가
- **Compliance (20%)**: 정책과 안전 규칙을 준수하는가
- **Resolution (15%)**: 고객 문제를 실제로 해결하는 방향인가
- **Communication (10%)**: 표현이 명확하고 친절한가

weight의 합이 정확히 1.0이라는 것은 테스트로 보장된다.

### Critical Override와 Grade Band의 분리

critical failure는 "이 답변은 점수를 매길 가치도 없이 위험하다"는 신호다.
grade band는 "점수를 매긴 뒤 어떤 등급에 해당하는가"를 분류한다.
이 둘은 다른 타이밍에 적용된다: critical은 계산 전, grade band는 계산 후.

### Judge 출력과 Final Score Merge 계약

judge는 각 축의 subscore와 failure types를 출력한다.
merge는 그 subscore에 weight를 곱해서 total을 계산한다.
이 분리 덕분에 judge를 교체해도 merge contract 테스트는 그대로 돌아간다.

## 참고 자료

### Quality Rubric Contract

- **경로**: `python/src/stage01/rubric.py`
- **왜 읽었나**: score 계산 규칙을 가장 작은 형태로 고정하기 위해
- **배운 것**: scoring vocabulary를 먼저 얼려두면 후속 실험이 **숫자 비교**로 귀결된다
- **이후 영향**: v1/v2 compare도 동일한 score axes를 공유하게 됨
