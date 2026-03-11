# 재현 가이드

## 실행 환경

- Python 3.8+
- Bash 셸

## 자동 테스트

```bash
cd problem
make test
```

## 기대 결과

- `script/test_rdt.sh`가 실행되고 RDT 3.0/GBN 관련 검증이 통과한다.

## 수동 재현

```bash
cd problem
make run-solution-rdt3
make run-solution-gbn
```

## 주의사항

- 데모 실행은 손실/손상률 설정에 따라 로그 패턴이 달라질 수 있다.
- 정답 구현은 `python/src/rdt3.py`, `python/src/gbn.py`를 기준으로 검증한다.
