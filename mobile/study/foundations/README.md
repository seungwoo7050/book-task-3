# foundations

`foundations`는 React Native 기본기를 단계적으로 고정하는 구간이다.
여기서는 "동작하는 화면"보다 상태 구조, 성능 측정, 상호작용 품질을 설명할 수 있는지에 초점을 둔다.

## 포함 프로젝트

1. [01-navigation-patterns](01-navigation-patterns/README.md)
2. [02-virtualized-list-performance](02-virtualized-list-performance/README.md)
3. [03-gestures-and-reanimated](03-gestures-and-reanimated/README.md)

## 왜 이 순서인가

- `01-navigation-patterns`는 화면 구조와 deep link를 먼저 고정한다.
- `02-virtualized-list-performance`는 리스트 성능과 측정 습관을 붙인다.
- `03-gestures-and-reanimated`는 UI thread 중심 상호작용 품질을 다룬다.

## 다음 단계

기초 화면 모델과 상호작용 품질을 이해한 뒤 [architecture](../architecture/README.md)에서
runtime 경계와 native boundary를 다룬다.
