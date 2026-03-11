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

- UDP 서버가 임시로 실행된 뒤 클라이언트 동작(응답/타임아웃/통계) 검증이 통과한다.

## 수동 재현

```bash
cd problem
make run-server
# 다른 터미널
make run-solution
```

## 주의사항

- 기본 포트는 `12000`이다.
- 서버는 패킷 손실을 시뮬레이션하므로 일부 핑은 타임아웃될 수 있다.
