# Verification And Boundaries

## 1. 자동 검증은 filter, index, combined lookup을 함께 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/06-index-filter/tests	(cached)
```

테스트가 잡는 항목은 아래와 같다.

- Bloom filter no false negative
- false positive rate upper bound
- sparse index block lookup
- SSTable Bloom reject
- SSTable bounded positive scan

즉 이 랩은 filter와 index를 별도 단위로도, 통합 table path로도 검증한다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
durian=gold bytes_read=74
```

추가 재실행 출력:

```text
miss false true true 0
hit true gold 74 0 74
footer SIF1 96 112 4
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- missing key는 Bloom reject로 0-byte read에서 끝난다
- hit key는 전체 data section이 아니라 좁은 block만 읽는다
- footer만으로 filter/index 위치와 block size를 복원할 수 있다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 production read-path optimization 전체로 읽으면 안 된다.

- learned index가 없다
- adaptive filter tuning이 없다
- block cache와 prefetch가 없다
- range scan 최적화가 없다
- false positive rate를 runtime telemetry로 수집하지 않는다

즉 현재 focus는 point lookup의 두 갈래 경로를 선명하게 드러내는 데 있다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "SSTable read path를 완성했다"
- "읽기 최적화를 충분히 끝냈다"
- "Bloom false positive를 실전 수준으로 튜닝했다"

현재 소스와 테스트가 실제로 보여 주는 것은 Bloom reject, sparse block range, footer-backed reopen, bounded bytes read까지다. 그보다 큰 최적화 claim은 근거가 없다.
