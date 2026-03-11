> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Selection Rubric & Eval Contract — 문제 정의

## 풀어야 하는 문제

추천 알고리즘이 "좋은 추천"을 하고 있는지 어떻게 판단하는가?
주관적 판단("이거 꽤 괜찮은데?")이 아니라, **수치로 측정 가능한 기준**이 필요하다.

## rubric이라는 접근

추천 품질을 여러 축으로 나눠서 각각 점수를 매기는 방식이다.

선택한 축:
- **relevance**: 추천된 도구가 요청과 얼마나 관련 있는가
- **rank accuracy**: 기대 순위와 실제 순위가 얼마나 일치하는가
- **coverage**: eval case 전체에서 정답 도구를 얼마나 커버하는가
- **diversity**: 추천 결과가 특정 카테고리에 편중되지 않는가

## offline eval contract

eval case를 실행하고 rubric에 따라 점수를 매기는 자동화된 계약이다.
사람이 매번 확인하지 않아도 `pnpm eval` 한 번이면 현재 추천 품질을 알 수 있다.

contract 구조:
1. eval.ts에서 eval case를 로드
2. 각 case에 대해 추천 알고리즘 실행
3. 추천 결과를 기대값과 비교
4. rubric 축별 점수 산출
5. threshold와 비교하여 pass/fail 판정

## acceptance threshold

- relevance ≥ 0.7 (70% 이상의 추천이 관련 있어야 함)
- rank accuracy ≥ 0.5 (1순위 정답률 50% 이상)
- 전체 eval pass rate ≥ 80%

이 threshold는 v0 baseline을 기준으로 설정했다. v1, v2에서 개선하며 올려간다.
