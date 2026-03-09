# Debug Log

## Current recorded issue

이 baseline capstone의 가장 큰 문제는 개별 기능 bug보다 “통합 스캐폴드”라는 성격을 얼마나 정직하게 드러내느냐였다.

- failing command or request:
  - none recorded as a blocking defect beyond standard validation
- exact symptom:
  - auth, catalog, cart, order가 모두 보이면 완성된 커머스 백엔드처럼 읽히기 쉽다
- first incorrect assumption:
  - feature surface가 넓으면 capstone의 완성도도 충분히 높아 보일 것이라고 생각하기 쉽다
- evidence collected:
  - README와 docs는 `verified scaffold`, payment omission, partial auth depth를 분명히 적는다

## Root cause

통합 캡스톤은 범위가 넓어서 구현 깊이가 쉽게 과대평가된다. baseline과 portfolio-grade capstone을 구분해 두지 않으면 학습 이력이 흐려진다.

## Fix and verification

- code or config change made:
  - baseline capstone 설명과 v2 승격판 설명을 분리했다
- why that change addresses the cause:
  - 독자가 baseline과 upgraded version의 역할 차이를 이해할 수 있다
- command, test, or log line that proved the fix:
  - `make lint`
  - `make test`
  - `make smoke`

## Follow-up debt

- baseline capstone 자체는 여전히 shallow integration이 남아 있다
- `commerce-backend-v2`와의 diff 문서를 따로 만들 수 있다

