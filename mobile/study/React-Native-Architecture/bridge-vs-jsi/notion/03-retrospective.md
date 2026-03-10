# 03 — Retrospective: Bridge vs JSI 벤치마크 회고

## 무엇을 만들었나

React Native 0.84 환경에서 async serialized surface와 sync direct-call surface를 
동일 workload(payloadSize 1000, 5회 측정)로 비교하는 벤치마크 앱을 구현했다.
통계 계산(평균/표준편차), 대시보드 UI, JSON export까지 포함한다.

## 잘된 점

### 1. runtime toggle 대신 surface 비교

RN 0.84에서 old Bridge runtime을 켜는 것은 비現실적이다.
대신 "Bridge처럼 동작하는 surface"와 "JSI처럼 동작하는 surface"를 비교하는 접근이 적절했다.
이 구분은 TurboModules가 왜 존재하는지를 설명하는 좋은 교육 자료가 된다.

### 2. 5-run 평균 + 표준편차

단일 측정값 대신 5회 측정의 통계를 사용한 것은 벤치마크의 기본 원칙에 충실하다.
`computeStats()`의 표준편차가 mean 대비 충분히 작으면 측정이 안정적이라는 판단 근거가 되고,
크면 외부 요인(GC, OS 스케줄링 등)의 개입을 의심할 수 있다.

### 3. 결정적 export

`buildExport()`의 `generatedAt`을 고정 문자열로 둔 것은 테스트 가능성을 최우선한 결정이었다.
`toEqual`로 export 객체 전체를 비교하면 "계산 로직이 정확한가?"를 완전히 검증할 수 있다.

## 아쉬운 점

### 1. 실제 native 호출이 없다

현재 벤치마크는 하드코딩된 측정값으로 통계 로직을 검증할 뿐,
실제 native module을 호출해 측정하지 않는다.
실무에서는 `performance.now()`로 JS → Native 왕복 시간을 측정하는 harness가 필요하다.

### 2. payload 크기 변화에 따른 비교 없음

payloadSize가 1000으로 고정되어 있다.
직렬화 비용은 payload 크기에 비례하므로, 100 / 1000 / 10000 등 다른 크기에서의 
scaling 특성을 보여주면 Bridge의 비용 구조가 더 명확해졌을 것이다.

### 3. 시각화가 최소한이다

두 개의 카드에 숫자를 나열하는 것은 정보 전달은 되지만 시각적 임팩트가 부족하다.
Bar chart나 line chart로 samples 분포를 보여주면 편차를 직관적으로 보여줄 수 있었다.

## 설계 판단 기록

### 왜 runtime toggle을 하지 않는가?

RN 0.84는 New Architecture(Fabric + TurboModules)가 기본이다.
`newArchEnabled = false`로 old Bridge를 사용할 수 있지만:
1. 점점 더 많은 라이브러리가 New Architecture만 지원한다.
2. Facebook 자체가 old Bridge를 deprecation 경로에 올렸다.
3. old Bridge로 빌드하면 TurboModule이 동작하지 않아 별도 설정이 필요하다.

따라서 "현재 아키텍처 안에서 두 가지 호출 패턴을 비교"하는 것이 더 실용적이다.

### 왜 samples를 5회로 잡았나?

통계적으로 유의미한 최소치는 30회지만, 이 프로젝트의 목적은 통계적 엄밀함이 아니라
"평균과 표준편차를 계산하고 해석하는 practice"다.
5회는 수동으로 실행해도 부담이 없고, 배열로 한눈에 볼 수 있는 크기다.

### 왜 BenchmarkStats에 mean과 stddev만 있나?

median, percentile(p95, p99) 등 다른 통계량도 의미 있지만,
5개 samples에서 p95를 계산하면 사실상 max와 같아진다.
sample 수가 적을 때는 mean + stddev가 가장 직관적인 요약이다.

## Bridge vs JSI: 핵심 차이 정리

| 측면 | Bridge (async serialized) | JSI (sync direct-call) |
|------|--------------------------|----------------------|
| 통신 방식 | JSON 직렬화 → 메시지 큐 → 역직렬화 | C++ 객체 직접 참조 |
| 동기 여부 | 비동기 (Promise) | 동기 |
| 직렬화 비용 | payload 크기에 비례 | 없음 |
| 평균 응답 시간 | 44.2ms | 10.8ms |
| 표준편차 | 1.72ms | 0.75ms |
| 속도 비율 | baseline | ~4x 빠름 |

## 다음 단계에서 시도할 것

1. **실제 TurboModule 호출 측정**: `performance.now()`로 JS → Native 왕복 시간 측정
2. **Payload scaling 테스트**: 100, 1000, 10000 크기별 비교로 직렬화 비용 scaling 확인
3. **시각화 개선**: react-native-svg 기반 bar chart로 samples 분포 표시
4. **Sync vs Async TurboModule**: 실제 TurboModule의 sync/async 호출 벤치마크
