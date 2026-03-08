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

- 프록시 서버가 임시로 실행된 뒤 테스트 스크립트가 통과한다.
- 테스트 종료 후 임시 프로세스가 자동 정리된다.

## 수동 재현

```bash
cd problem
make run-solution
# 다른 터미널
curl -x http://localhost:8888 http://www.example.com/
```

## 주의사항

- 기본 포트는 `8888`이다.
- 캐시 상태를 초기화하려면 `make clean`으로 `cache/`를 정리한다.
