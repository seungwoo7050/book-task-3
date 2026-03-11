# 재현 가이드

## 실행 환경

- Bash 셸
- `make`
- (선택) Wireshark 또는 tshark

## 정답 검증 실행

```bash
cd problem
make test
```

## 기대 결과

- `script/verify_answers.sh`가 실행되고 답안 완결성 검증이 통과해야 한다.

## 검증 흐름

1. `problem/README.md`에서 질문 세트를 확인한다.
2. `docs/` 문서로 TCP/UDP 개념과 분석 필터를 정리한다.
3. `analysis/src/tcp-udp-analysis.md`에 패킷 번호와 필드 값을 근거로 정리한다.
4. `make test`로 최종 검증을 수행한다.

## 주의사항

- 이 실습은 캡처 파일 분석 기반이다.
- 답안은 Markdown 문서(`tcp-udp-analysis.md`) 형식으로 관리한다.
