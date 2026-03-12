# Typed Navigation Params

ParamList는 네비게이터 계약이다.
문서와 구현이 따로 놀지 않게 하려면 route params shape를 타입으로 먼저 잠그는 편이 낫다.

## Benefits

- `navigate()` 호출 시 잘못된 파라미터 shape를 바로 막을 수 있다
- screen component가 어떤 route params를 기대하는지 코드에서 드러난다
- deep-link state hydration이 어떤 값을 보완해야 하는지도 명확해진다

## In This Pilot

- `HomeStackParamList`가 `Detail`, `ProfileDetail` params를 고정한다
- `ProfileStackParamList`가 profile tab 내부 흐름을 고정한다
- root 수준에서는 `NavigatorScreenParams`로 nested navigator state를 합성한다
