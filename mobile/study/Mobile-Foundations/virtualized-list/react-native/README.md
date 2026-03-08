# React Native Implementation

Status: verified

이 앱은 10k dataset, FlatList baseline, FlashList v2 optimized view, benchmark summary를 한 번에 보여 주는 독립 React Native CLI 앱이다.

## Commands

```bash
npm install
npm run typecheck
npm test
npm run benchmark
npm run verify
```

## Covered Behaviors

- deterministic dataset generation
- FlatList baseline rendering
- FlashList v2 optimized rendering
- cursor-style pagination state
- benchmark summary export

## Limits

- 저장소 공용 gate는 JS/type/test와 benchmark summary export다.
- 실제 device profiler 캡처는 추가 evidence이지 필수 gate가 아니다.
