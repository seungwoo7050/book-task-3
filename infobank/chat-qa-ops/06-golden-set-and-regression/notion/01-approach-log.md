# 06-golden-set-and-regression 접근 기록

## 이 stage의 질문

개선 실험이 실제 품질 향상인지 어떻게 데이터셋과 manifest로 증빙할 것인가?

## 선택한 방향

- golden cases와 compare manifest를 별도 JSON 파일로 분리했다. 이유: 데이터셋 내용과 비교 대상 메타데이터가 서로 다른 변경 주기를 가지기 때문이다.
- assertion 실패는 `MISSING_REQUIRED_EVIDENCE_DOC` 같은 reason code를 사용한다. 이유: v2의 개선 효과를 failure type 감소로 직접 비교하기 위해서다.

## 제외한 대안

- 비교 대상을 테스트 코드에 하드코딩하는 방식
- pass/fail만 남기고 failure reason을 버리는 방식

## 선택 기준

- golden case는 required evidence 문서를 명시한다.
- assertion 실패는 reason code로 설명된다.
- baseline과 candidate label을 manifest 파일로 고정한다.

## 커리큘럼 안에서의 역할

- v1 compare와 v2 improvement report의 최소 구조를 stage 단위로 축소한 것이다.
- evidence miss 감소를 수치로 논증하려면 manifest와 assertion이 함께 있어야 한다.

## 아직 열어 둔 판단

이 pack은 sample-size가 작아 통계적 의미를 주장하기보다 compare 구조를 설명하는 데 초점이 있다.
