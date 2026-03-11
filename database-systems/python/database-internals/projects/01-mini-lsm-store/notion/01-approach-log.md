# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### 읽기 우선순위를 메모리에서 디스크 순으로 고정한다
- 관련 파일: `../src/mini_lsm_store/store.py`
- 판단: 최근 write가 항상 먼저 보이도록 active memtable, immutable snapshot, newest-first SSTable 순서로 읽습니다. 이 순서가 LSM read path의 핵심 계약입니다.

### flush 동안 immutable snapshot을 분리한다
- 관련 파일: `../src/mini_lsm_store/store.py`
- 판단: active memtable을 바로 비워 버리는 대신 immutable snapshot으로 떼어 놓고 파일화합니다. 이렇게 해야 flush 중에도 읽기 규칙을 설명할 수 있습니다.

### 학습용 포맷은 단순하게, precedence는 엄격하게 가져간다
- 관련 파일: `../src/mini_lsm_store/store.py`
- 판단: on-disk 포맷은 JSON lines로 단순화하되, read precedence와 tombstone masking 규칙은 느슨하게 만들지 않습니다.

## 검증 명령
```bash
cd python/database-internals/projects/01-mini-lsm-store
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m mini_lsm_store
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- memtable, immutable snapshot, SSTable 세 계층을 그림으로 놓고 read precedence를 설명하면 이 프로젝트의 핵심이 바로 전달됩니다.
- flush 이후에도 같은 key lookup 결과가 유지된다는 점을 demo와 test로 같이 보여 줄 수 있습니다.
- JSON lines 포맷으로 디버깅 난도를 낮추면서도 precedence 규칙은 엄격하게 유지했다는 점도 설명 포인트가 됩니다.
