# 00. 문제 정의

## 문제를 어떻게 이해했는가

`perflab`은 정답 함수 두 개를 만드는 프로젝트가 아니라,
"캐시 miss를 설명 가능한 방식으로 줄이는 법"을 묻는 프로젝트라고 봤다.

그래서 저장소도 다음 두 층을 분명히 했다.

- Part A: trace-driven cache simulator
- Part B: miss 기반 transpose 최적화

## 저장소 기준 성공 조건

- sample trace oracle이 고정돼 있다
- transpose가 세 크기 모두에서 정답을 만든다
- naive보다 miss가 줄어든다
- benchmark 기준이 wall-clock time이 아니라 miss count로 설명된다

## 선수 지식

- set/tag/offset 분해
- LRU 교체
- direct-mapped cache
- blocking 전치와 diagonal conflict
