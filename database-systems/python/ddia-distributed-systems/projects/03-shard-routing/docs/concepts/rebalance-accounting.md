# Rebalance Accounting

consistent hashing의 핵심 가치는 membership 변화가 있을 때 전체 key를 거의 다 움직이지 않는다는 점이다. 그래서 구현을 검증할 때는 "새 ring이 얼마나 적은 key를 옮겼는가"를 함께 본다.

이 프로젝트는 key 집합에 대한 기존 assignment map과 새 ring의 assignment를 비교해서 moved key 수를 계산한다. add/remove가 일어나도 moved ratio가 전체의 절반 이하로 유지되는지를 테스트한다.
