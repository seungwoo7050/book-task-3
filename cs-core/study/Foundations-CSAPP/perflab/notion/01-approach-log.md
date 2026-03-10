# 01. 접근 기록

## 실제로 택한 접근

이 프로젝트는 성능 최적화를 바로 하지 않았다.

1. cache simulator의 oracle 결과 먼저 고정
2. transpose의 naive 기준선 확인
3. `32x32`, `64x64`, `61x67`를 분리해서 접근
4. threshold와 실제 miss를 함께 기록

## 왜 이 순서를 택했는가

- simulator가 틀리면 뒤 benchmark 해석도 의미가 없다
- transpose는 크기마다 conflict 패턴이 달라서 하나의 전략으로 묶기 어려웠다
- miss 기준을 먼저 정해 두면 설명이 짧아진다
