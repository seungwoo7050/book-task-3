# Source Brief — 접근 기록

## reference spine 구성

프로젝트의 참조 문서를 결정해야 했다.
후보가 많았지만, 최종적으로 두 가지 문서로 정리했다:

1. **reference-spine.md**: 추천 시스템의 참조 구조 (selector, reranker, evaluator, gate)
2. **project-selection-rationale.md**: MCP 추천을 선택한 이유 (한국어 시장, 도구 증가 추세, 운영 필요성)

나머지 문서들은 각 stage의 docs/에 분산시켰다.
이 결정의 장점: source brief가 짧고 명확하다.

## catalog seed 결정

catalog.ts에 넣을 MCP 도구를 선정했다.
실제 운영 가능한 도구 목록보다는 **추천 알고리즘의 다양한 케이스를 커버하는** 조합을 목표로 했다.

선정 기준:
- 카테고리가 다양해야 한다 (dev-tools, data, docs, monitoring)
- 한국어 노출 필드가 있는 도구와 없는 도구가 섞여야 한다
- semver 버전이 달라야 compatibility gate를 테스트할 수 있다
- 일부는 deprecated 상태여야 release gate를 테스트할 수 있다

결과: github-repo-inspector, postgres-schema-mapper, korean-docs-search 등 10+ 도구를 seed에 포함했다.

## eval fixture 설계

eval.ts의 offline eval case를 설계했다.
각 case는:
- 입력: 사용자 요청 텍스트 + 맥락 정보
- 기대 출력: 추천되어야 할 도구 ID + 순위

case를 설계할 때 가장 어려웠던 건, **올바른 정답이 하나가 아닌 경우**다.
"릴리즈 체크"라는 요청에 release-check-bot이 1순위, github-repo-inspector가 2순위일 수 있다.
그래서 eval case에 순위(rank)를 포함시켰다.
