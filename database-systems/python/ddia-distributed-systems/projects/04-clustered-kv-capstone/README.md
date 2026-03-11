# 04 Clustered KV Capstone

정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store로 routing, replication, disk-backed storage를 한 흐름으로 연결합니다.

## 문제

- key를 shard로 라우팅하고 shard별 leader/follower group을 선택해야 합니다.
- leader write가 log-backed 또는 disk-backed store에 기록돼야 합니다.
- follower가 watermark 이후 entry만 catch-up해야 합니다.
- node restart 뒤에도 disk에서 상태를 복원해야 합니다.
- leader read와 follower read가 모두 가능해야 합니다.

## 내 해법

- router, leader, follower, local store가 한 write pipeline 안에서 어떻게 연결되는지 익힙니다.
- 정적 topology만으로도 shard routing과 follower catch-up을 묶어 볼 수 있음을 확인합니다.
- storage engine과 distributed path를 한 저장소 안에서 통합하는 감각을 익힙니다.

## 검증

```bash
cd python/ddia-distributed-systems/projects/04-clustered-kv-capstone
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m clustered_kv
```

## 코드 지도

- `problem/README.md`: 문제 정의, 제약, 제공 자료, provenance를 확인하는 시작점입니다.
- `docs/README.md`: 개념 메모와 참고자료 인덱스를 먼저 훑는 문서입니다.
- `src/`: 핵심 구현 패키지와 `__main__` entry point가 들어 있습니다.
- `tests/`: pytest 기반 회귀 테스트를 모아 둔 위치입니다.
- `notion/README.md`: 현재 공개용 학습 노트와 설계 로그의 입구입니다.
- `notion-archive/README.md`: 이전 세대 문서를 보존하는 아카이브입니다.

## 읽는 순서

- `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
- `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
- `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: dynamic membership, automatic failover, consensus 기반 leader election은 포함하지 않습니다.
- 현재 범위 밖: production deployment와 운영 자동화는 포트폴리오 확장 범위로 남깁니다.
- 확장 아이디어: 관리 API, observability, fault injection을 추가하면 공개 포트폴리오 프로젝트로 발전시키기 좋습니다.
- 확장 아이디어: control plane, membership change, consensus를 붙이면 실제 분산 KV 설계로 확장할 수 있습니다.
