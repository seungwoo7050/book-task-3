# React Native Implementation

Status: verified

이 앱은 swipe, reorder, shared transition을 하나의 interaction playground로 묶은 React Native CLI 구현이다.

## Commands

```bash
npm install
npm run typecheck
npm test
npm run verify
```

## Covered Behaviors

- swipe threshold + spring back
- reorder helper math
- shared transition style detail flow
- dismiss progress interpolation

## Limits

- UI-thread fidelity는 디바이스에서 확인하는 추가 evidence이고, 저장소 공용 gate는 JS/type/test다.
