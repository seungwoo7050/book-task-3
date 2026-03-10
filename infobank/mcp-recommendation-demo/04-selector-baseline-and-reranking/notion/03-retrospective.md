# 04 baseline selector와 reranking 회고

## 이번 stage로 좋아진 점

- 추천 로직이 단계적으로 진화했다는 점을 버전별로 설명할 수 있다.
- 학생이 baseline과 candidate를 분리해 개선 증빙 구조를 만들 수 있다.
- compare 결과가 다음 stage의 로그/지표 설계와 자연스럽게 이어진다.

## 아직 약한 부분

- 별도 stage 구현이 없으므로 실제 동작은 capstone 버전으로 내려가 확인해야 한다.
- 이 단계는 '더 똑똑한 추천'을 만들었다는 주장보다, 왜 그렇게 판단할 수 있는지의 근거를 정리한다.

## 학생이 여기서 바로 가져갈 것

- baseline과 candidate를 같은 입력셋 위에서 비교하는 문서 구조
- reranking 실험을 코드와 compare proof 둘 다로 남겨 설명력을 높이는 방식

## 05-development-timeline.md와 같이 읽을 포인트

- 타임라인에서 `v0` baseline과 `v1` rerank 경로를 순서대로 읽어, 개선의 기준면을 먼저 잡는다.
- compare snapshot을 볼 때는 uplift 숫자보다 baseline 보존과 candidate 설명력 확대를 함께 본다.

## 나중에 다시 볼 것

- baseline 대비 candidate 개선을 설명하는 구조
- reranking 실험을 문서와 테스트로 함께 남기는 방식
