# Distance-Vector Routing — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
# 표준 라이브러리: json, copy, sys
# 테스트: pytest
pip install pytest
```

## Phase 1: 토폴로지 로더

**작업 함수**: `load_topology(filepath: str)`

1. JSON 파일 읽기: `json.load()`
2. 노드 리스트 추출: `data["nodes"]`
3. 인접 리스트 구성: `adj[node] = {neighbor: cost}`
4. 양방향(무향) 그래프로 처리

**테스트 데이터**:
- `problem/data/topology.json` — 3노드 (x, y, z)
- `problem/data/topology_5node.json` — 5노드

```bash
python3 -c "
import json
with open('problem/data/topology.json') as f:
    print(json.dumps(json.load(f), indent=2))
"
```

## Phase 2: DVNode 클래스

**작업 파일**: `python/src/dv_routing.py`

### 초기화 (`__init__`)
1. distance_vector: 자기 자신=0, 이웃=링크비용, 나머지=INF
2. next_hop: 이웃은 해당 이웃, 나머지=None
3. neighbor_dvs: 이웃에게 받은 DV 저장소 (비어있음)

### receive_dv 메서드
1. 이웃 DV를 deep copy로 저장
2. 모든 destination에 대해 Bellman-Ford 업데이트:
   `cost_via_v = link_cost + neighbor_dv.get(dest, INF)`
3. 더 작은 비용 발견 시 DV, next_hop 갱신
4. 변경 여부 반환 (수렴 판정용)

### 출력 메서드
- `format_dv()`: `Node x: {x: 0, y: 2, z: 3}`
- `format_routing_table()`: `Node x: to y cost 2 via y | to z cost 3 via y`

## Phase 3: 시뮬레이션 루프

**작업 함수**: `simulate(topology_file: str)`

1. 토폴로지 로드 → 노드 생성
2. 초기 상태 출력 (Iteration 0)
3. 반복:
   - Phase 1: 모든 노드의 DV 수집 (`get_dv()` — deep copy)
   - Phase 2: 각 노드가 이웃의 DV 수신 → `receive_dv()`
   - 변경 여부 추적
   - 현재 상태 출력
   - 변경 없으면 "Converged" 출력 후 break
4. 최종 라우팅 테이블 출력
5. 안전 제한: `max_iterations = len(nodes) * 10`

**CLI 확인**:
```bash
python3 python/src/dv_routing.py problem/data/topology.json
# → Iteration 0, 1, ... → Converged → 라우팅 테이블
```

## Phase 4: CLI 인터페이스

```python
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dv_routing.py <topology.json>")
        sys.exit(1)
```

## Phase 5: 다중 토폴로지 테스트

```bash
# 3노드 테스트
python3 python/src/dv_routing.py problem/data/topology.json

# 5노드 테스트
python3 python/src/dv_routing.py problem/data/topology_5node.json
```

## Phase 6: 테스트 및 검증

```bash
# 자동 테스트
make -C problem test
# → test_routing.sh가 여러 토폴로지에 대해 출력 검증

# pytest
cd python/tests && python3 -m pytest test_dv_routing.py -v
```

## 최종 파일 구조

```
routing/
├── python/
│   ├── src/dv_routing.py           ← 솔루션 (200줄)
│   └── tests/test_dv_routing.py    ← pytest
├── problem/
│   ├── Makefile                    ← make test / make run-solution
│   ├── code/dv_skeleton.py         ← 제공 skeleton
│   ├── data/
│   │   ├── topology.json           ← 3노드 토폴로지
│   │   └── topology_5node.json     ← 5노드 토폴로지
│   └── script/test_routing.sh      ← 검증 스크립트
├── docs/concepts/
└── notion/                         ← 이 문서
```
