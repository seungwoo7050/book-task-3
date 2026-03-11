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

- 서버가 임시로 실행되고 `script/test_server.sh` 검증이 통과한다.

## 수동 재현

```bash
cd problem
make run-solution
# 다른 터미널
curl -v http://localhost:6789/hello.html
curl -v http://localhost:6789/nonexistent.html
```

## 주의사항

- 기본 포트는 `6789`이다.
- 서버는 `problem/data/`를 기준으로 파일을 서빙한다.
