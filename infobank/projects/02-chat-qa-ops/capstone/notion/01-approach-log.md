# capstone 접근 기록

## 이 stage의 질문

상담 품질 관리 플랫폼을 runnable demo, regression hardening, improvement proof까지 포함한 제출물로 어떻게 마감할 것인가?

## 선택한 방향

- 버전은 폴더 단위 snapshot으로 유지했다. 이유: v0, v1, v2의 역할과 검증 결과를 분리해 학습 기록과 제출 증빙을 동시에 보존하기 위해서다.
- v1은 안정화, v2는 retrieval improvement proof에 집중하도록 역할을 고정했다. 이유: 한 버전에서 너무 많은 축을 동시에 바꾸면 compare 결과 해석이 어려워진다.
- provider chain은 Upstage Solar 우선, OpenAI 보조, Ollama fallback 구조로 유지했다. 이유: 한국어 성능, 상용 API 호환성, 로컬 fallback을 함께 확보하려는 요구와 맞기 때문이다.

## 제외한 대안

- v0 폴더를 직접 계속 수정하는 in-place versioning
- 개선 실험과 안정화 작업을 한 버전에 동시에 몰아넣는 방식
- live provider 검증 없이는 전체 저장소를 설명할 수 없다고 보는 방식

## 선택 기준

- v0, v1, v2가 각자 독립적으로 runnable하고 역할이 다르다.
- compare는 같은 dataset과 run label 위에서 baseline 대비 개선을 증빙한다.
- fallback, dependency health, dashboard, proof artifact가 공개 저장소 기준으로 재현 가능하다.

## 커리큘럼 안에서의 역할

- 이 항목 자체가 최종 제출물이다.
- tracked docs는 stable index 역할을 하고, notion은 process-heavy technical notebook 역할을 한다.

## 아직 열어 둔 판단

live Upstage/OpenAI/Langfuse 호출은 이 저장소에서 기본 검증 경로에 포함하지 않았다. 현재 증빙은 mock/no-op와 local fallback을 기준으로 한다.
