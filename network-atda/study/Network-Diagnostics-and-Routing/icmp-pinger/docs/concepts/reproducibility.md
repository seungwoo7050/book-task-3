# 재현 가이드

## 실행 환경

- Python 3.8+
- Bash 셸
- 기본 canonical test는 root 불필요
- live raw-socket 실행은 root 권한 필요

## 자동 테스트

```bash
cd problem
make test
```

## 기대 결과

- checksum, packet build, synthetic raw-socket flow 검증이 통과한다.
- 비권한 환경에서도 동일한 결과를 재현할 수 있다.

## 수동 재현

```bash
cd problem
sudo make run-solution HOST=google.com
sudo make test-live HOST=google.com
```

## 주의사항

- 네트워크/방화벽 정책에 따라 ICMP 응답이 제한될 수 있다.
- CI/샌드박스 환경에서는 live raw-socket 실행 대신 `make test`를 기준으로 본다.
