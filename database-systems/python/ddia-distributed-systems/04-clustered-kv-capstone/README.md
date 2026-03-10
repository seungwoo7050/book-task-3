# 04 Clustered KV Capstone

정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store로 routing, replication, disk-backed storage를 한 흐름으로 연결합니다.

## 이 프로젝트에서 배우는 것

- router, leader, follower, local store가 한 write pipeline 안에서 어떻게 연결되는지 익힙니다.
- 정적 topology만으로도 shard routing과 follower catch-up을 묶어 볼 수 있음을 확인합니다.
- storage engine과 distributed path를 한 저장소 안에서 통합하는 감각을 익힙니다.

## 먼저 알고 있으면 좋은 것

- routing, replication, local storage 개념을 이미 한 번씩 읽어 두는 것이 좋습니다.
- Python 버전은 FastAPI를 서비스 경계로만 사용하므로 HTTP boundary 감각이 있으면 도움이 됩니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `src/clustered_kv/`, `tests/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd python/ddia-distributed-systems/04-clustered-kv-capstone
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m clustered_kv
```

## 구현에서 집중할 포인트

- leader write가 local disk-backed store와 follower catch-up으로 자연스럽게 이어지는지 확인합니다.
- 정적 topology 제약 안에서 read/write 경로가 충분히 설명되는지 봅니다.
- 테스트와 demo에서 node restart 후 state 복원이 드러나는지 확인합니다.

## 포트폴리오로 발전시키려면

- 관리 API, observability, fault injection을 추가하면 공개 포트폴리오 프로젝트로 발전시키기 좋습니다.
- control plane, membership change, consensus를 붙이면 실제 분산 KV 설계로 확장할 수 있습니다.
