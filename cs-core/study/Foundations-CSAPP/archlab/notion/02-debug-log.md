# 02. 디버그 기록

## 실제로 다시 확인한 포인트

### 1. `iaddq`의 condition code 갱신 누락

결과 값을 `rB`에 쓰는 것만 맞추면 될 것 같지만,
condition code를 산술 연산처럼 갱신하지 않으면 바로 틀린다.

### 2. HCL patch 적용 위치 혼동

Part B와 Part C의 수정 포인트를 섞으면 검증이 애매해진다.
그래서 patch logic를 파일로 분리한 것이 유효했다.

### 3. Part C에서 correctness와 성능 판단을 섞는 문제

optimized `ncopy`는 "더 빠르다" 전에 "여전히 같은 결과를 만든다"가 먼저다.
Pseudo-CPE는 그 다음 설명 도구여야 한다.

### 4. 공식 benchmark 수치 해석

`Average CPE 9.16`, `Score 26.8/60.0`는 절대적 정답이 아니라 현재 상태 기록이다.
문서에서는 맥락 없이 수치만 남기지 않도록 주의했다.
