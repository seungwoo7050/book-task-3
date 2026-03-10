# Architecture Lab을 세 파트로 나눠 읽어야 하는 이유

## 한 과제로 보이지만 실제로는 세 종류의 문제다

Architecture Lab은 이름은 하나지만, 실제로는 서로 다른 질문을 던집니다.

- Part A: Y86-64로 의미를 직접 구현할 수 있는가
- Part B: 새 명령어를 합법적으로 만드는 제어 신호를 이해하는가
- Part C: 같은 의미를 유지하면서 pipeline 관점에서 더 빠르게 만들 수 있는가

이 차이를 분리하지 않으면 프로젝트 구조가 금방 섞입니다.

## 저장소에서 어떻게 나눴는가

| 공식 파트 | 저장소의 대응 위치 |
|---|---|
| Part A Y86 프로그램 | `y86/src/*.ys` |
| Part B `iaddq` 제어 로직 | `y86/script/apply_hcl_patches.py`와 companion model |
| Part C `ncopy` 최적화 | `y86/src/ncopy.ys`와 C/C++ pseudo-cost model |

즉, 공식 hand-in 성격 산출물은 `y86/`에, 개념 보조 모델은 `c/`와 `cpp/`에 분리했습니다.

## 왜 이 분리가 학습에 좋은가

- 공식 산출물은 과제 감각을 살린다
- companion model은 추적 가능한 코드와 테스트를 남긴다
- 공개 저장소에서는 로컬 복원 자산에 의존하지 않는 설명 흐름을 확보할 수 있다

## 읽기 순서 추천

1. `problem/README.md`로 공식 경계 파악
2. 이 문서로 Part A/B/C 역할 정리
3. `y86/README.md`에서 실제 hand-in 산출물 확인
4. `c/`, `cpp/`에서 의미 모델과 테스트 읽기
