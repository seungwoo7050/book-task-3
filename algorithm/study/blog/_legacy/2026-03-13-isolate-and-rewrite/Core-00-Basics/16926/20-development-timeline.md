# BOJ 16926 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 써넣기 순서와 edge case를 점검한다.
- 진행: 추출할 때와 같은 인덱스 순서로 `ring[idx]`를 써넣으면 된다. 처음엔 추출 순서와 써넣기 순서를 따로 구현했다가, 같은 인덱스 루프를 재사용하는 게 안전하다는 걸 알았다.
- 이슈: N=2, M=2이면 레이어 1개, ring 길이 4. N=1 또는 M=1이면 layers=0이라 아무 회전도 안 한다.

### Session 4
- 검증: fixture 통과 확인.

CLI:

```bash
$ make -C study/Core-00-Basics/16926/problem test
```

```text
Test 1: PASS
Test 2: PASS
Results: 2/2 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제의 핵심은 "2차원 회전을 1차원 시프트로 변환"하는 아이디어다.
  - 가장 실수하기 쉬운 지점은 테두리 인덱스다. 네 변의 시작/끝 인덱스가 각각 다르고, 코너를 중복 포함하면 ring 길이가 틀어진다.
  - R을 모듈러하는 건 사소해 보이지만, 안 하면 R=10억에서 시간 초과가 된다.
