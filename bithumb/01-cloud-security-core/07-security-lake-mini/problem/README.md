# 문제 정리

## 문제 요약

Security Lake 개념을 로컬로 축소 구현해, 로그를 저장하고 미리 정의한 detection query로 이상 행위를 찾습니다.

## 입력

- CloudTrail fixture JSON
- 출력 lake 경로
- Parquet 경로

## 출력

- DuckDB lake
- Parquet 파일
- alert 결과

## 학습 포인트

적재와 탐지가 하나의 흐름으로 이어진다는 점을 작은 규모에서 체감하는 데 있습니다.
