# 01-quality-rubric-and-score-contract 접근 기록

## 이 stage의 질문

정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?

## 선택한 방향

- rubric과 grade band를 judge로부터 분리했다. 이유: judge 구현이 heuristic이든 LLM이든 최종 점수 체계는 동일해야 했기 때문이다.
- critical failure를 별도 branch로 처리했다. 이유: 가중 평균 안에서 critical severity를 표현하면 설명 가능성과 회귀 검증이 약해진다.

## 제외한 대안

- judge 프롬프트가 자유롭게 총점을 반환하도록 두는 방식
- grade band 없이 raw score만 저장하는 방식

## 선택 기준

- weight 총합이 1.0으로 유지된다.
- critical failure는 어떤 점수보다 우선한다.
- grade band가 후속 stage와 capstone에서 재사용 가능하다.

## 커리큘럼 안에서의 역할

- v0~v2 모두 같은 scoring vocabulary를 사용한다.
- dashboard overview의 평균 점수와 grade 분포는 이 contract를 전제로 해석된다.

## 아직 열어 둔 판단

weight 값 자체가 인간 평가자 합의로 교정된 것은 아니다. 이 단계는 calibration보다 contract freeze가 목적이다.
