# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- Y86-64와 C 유사 의사코드 매핑: instruction semantics를 고수준 동작으로 바꿔 읽어야 Part A/B/C가 한 줄로 이어진다.
- `iaddq`가 건드리는 stage: fetch, decode, execute, write-back 어디를 수정하는지 구분해야 patch 범위가 통제된다.
- condition code 갱신 조건: 모든 연산이 아니라 특정 경로에서만 CC를 써야 regression을 막을 수 있다.
- pipeline stall과 bubble: 성능 문제를 풀 때도 정답은 결국 hazard를 어떻게 줄였는지로 설명된다.
- pseudo-CPE와 공식 benchmark의 관계: 숫자 하나만 외우지 말고 왜 그 수치가 나왔는지 비용 모델로 연결해야 한다.

## 재현 중 막히면 먼저 확인할 것

- Part 분해: `../docs/concepts/part-split.md`
- 제어 신호 정리: `../docs/concepts/iaddq-and-control-signals.md`
- 비용 모델: `../docs/concepts/pipeline-cost-model.md`
- 현재 검증 순서: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- 구조를 먼저 나누고 성능을 마지막에 올리는 순서는 `perflab`과 시스템 구현 과제 전반에도 그대로 적용된다.
- 성능 수치는 항상 환경 차이를 타므로, 수치 자체보다 개선 이유를 남기는 편이 오래 간다.
