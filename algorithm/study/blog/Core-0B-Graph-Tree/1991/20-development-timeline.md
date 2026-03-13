# BOJ 1991 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case를 점검한다.
- 진행: N=1이면 루트 A 하나. 세 순회 모두 "A"를 출력한다.
- 이슈: result 리스트를 각 순회 사이에 `clear()`해야 한다. 처음엔 빼먹었다가 세 결과가 합쳐져서 출력됐다.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-0B-Graph-Tree/1991/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 세 순회의 차이는 `append` 위치 하나다. 이걸 코드로 직접 확인하니까 교과서 설명보다 명확했다.
  - 트리를 딕셔너리로 표현하는 게 배열 기반보다 간단하다. 노드가 알파벳 한 글자라서 인덱싱 변환이 필요 없다.
  - result를 clear하는 걸 빼먹은 실수는 테스트를 돌려보자마자 잡혔다.
