# 0x11 Amortized Analysis Lab — 문제 프레이밍

## 첫인상

CLRS Ch 17 분할 상환 분석. Stack MULTIPOP과 Binary Counter 두 가지 예제를 하나의 CLI로 비교한다. 추상적인 amortized 주장을 실제 연산 로그와 총 actual cost로 연결.

## 프로젝트 구조

`STACK` 모드와 `COUNTER` 모드. 각각 연산 수행 후 actual_cost, 최종 상태를 출력.

## 왜 이 프로젝트인가

분할 상환은 "최악 연산이 비싸도 총합은 저렴"이라는 직관을 수학적으로 보이는 기법. 직접 비용을 세보면서 체감.
