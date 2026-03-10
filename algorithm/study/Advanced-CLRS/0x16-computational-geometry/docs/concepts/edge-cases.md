# 경계 사례 점검

- 빈 구조나 단일 원소 입력도 정상 동작해야 한다.
- deterministic output order를 먼저 고정해서 fixture diff가 흔들리지 않게 한다.
- 입력 파서가 mode별 분기와 trailing newline을 안전하게 처리해야 한다.
