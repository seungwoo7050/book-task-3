# 00 — Problem Framing: Bridge vs JSI 벤치마크

## 문제의 출발점

React Native의 아키텍처는 "JS와 Native 사이의 통신"이 핵심이다.
전통적인 Bridge 방식은 JSON 직렬화를 거쳐 비동기로 메시지를 주고받았고,
JSI(JavaScript Interface)는 C++ 레벨에서 JS 런타임에 직접 바인딩해 동기 호출을 가능하게 했다.

React Native 0.84는 New Architecture가 기본이다.
old runtime을 토글하는 것은 더 이상 의미 있는 비교가 아니다.
대신 이 프로젝트는 **같은 workload를 두 가지 호출 surface에 적용해 성능 차이를 측정**한다:

1. **async serialized** — Promise 기반, payload copy를 흉내 내는 surface. Bridge 스타일의 통신 패턴을 시뮬레이션한다.
2. **sync direct-call** — 즉시 값을 반환하는 JSI 스타일 호출. 직렬화 없이 직접 접근한다.

## 왜 이 비교가 중요한가

1. **성능 차이를 체감이 아닌 숫자로 이해해야 한다** — "JSI가 빠르다"는 말은 쉽지만, 얼마나 빠른지, 어떤 조건에서 차이가 커지는지를 정량적으로 알아야 기술 선택에 근거가 생긴다.

2. **직렬화 비용은 payload 크기에 비례한다** — 작은 데이터에서는 차이가 미미하지만, 대량 데이터 전송에서는 Bridge의 직렬화/역직렬화 오버헤드가 지배적이 된다.

3. **TurboModules의 동작 원리를 이해하는 기초** — RN 0.84의 TurboModules는 JSI 위에 구축되어 있다. Bridge와 JSI의 차이를 이해해야 TurboModule이 왜 필요한지 설명할 수 있다.

## 설계 방향

### 벤치마크 모델

`BenchmarkRun` 하나가 5회 측정(samples)의 원시 데이터를 담는다.
두 개의 run이 존재한다:
- `async serialized` (payloadSize: 1000, samples: [42, 45, 44, 47, 43])
- `sync direct-call` (payloadSize: 1000, samples: [11, 10, 12, 10, 11])

동일한 payloadSize를 사용해 통제 변인을 맞추고,
5회 측정으로 평균과 표준편차를 계산해 단일 측정의 노이즈를 줄인다.

### 통계 계산

`computeStats(run)` 함수가 평균(mean)과 표준편차(stddev)를 계산한다.
소수점 둘째 자리까지 반올림해 표시용 수치를 생성한다.

### 결과 공유

`buildExport()` 함수가 모든 run의 통계를 모아 `generatedAt` 날짜와 함께 JSON 객체를 만든다.
`scripts/export-results.mjs`가 이 데이터를 `exports/benchmark-results.json`으로 저장한다.

## 학습 범위

| 영역 | 구체적 목표 |
|------|-------------|
| Bridge 이해 | JSON 직렬화 기반 비동기 통신의 비용 이해 |
| JSI 이해 | C++ 직접 바인딩, 동기 호출의 이점 이해 |
| 통계 | 5-run 평균/표준편차 계산, 결과 재현성 |
| 시각화 | 두 surface의 지표를 나란히 비교하는 대시보드 |
| Export | 결정적 JSON 파일 생성, CI 게이트 통합 |
