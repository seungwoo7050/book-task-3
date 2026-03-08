# FlashList v2 Benchmarking

이 과제는 같은 10k dataset을 `FlatList`와 `FlashList`에 적용해 baseline과 optimized를 비교한다.

## Measured Summary

- initial render time
- average FPS estimate
- blank-area estimate
- peak memory estimate
- cell mount count

## Why The App Uses Synthetic Metrics

저장소 공용 게이트는 JS/type/test다.
그래서 benchmark summary는 앱 내부의 결정적 sample metric 집합을 기준으로 계산하고,
디바이스 실측은 추가 evidence로만 문서화한다.

## FlashList v2 Notes

- cell type 분리가 recycling 효율에 직접 연결된다.
- list item height를 data type과 함께 관리하면 baseline/optimized 비교가 단순해진다.
- benchmark summary는 절대 FPS보다 baseline 대비 개선 폭을 먼저 보여 준다.
