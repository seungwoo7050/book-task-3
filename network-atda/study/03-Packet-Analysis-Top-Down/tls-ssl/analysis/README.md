# 공개 답안 안내

## 이 폴더의 역할
이 디렉터리는 `TLS Packet Analysis`의 공개 답안과 핵심 근거 문서를 담습니다. 프로젝트 README에서 문제를 확인한 뒤, 실제 답은 여기서 읽습니다.

## 먼저 볼 파일
- `analysis/src/tls-ssl-analysis.md` - 질문별 답안과 근거를 확인합니다.

## 기준 명령
- 검증: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`

## 현재 범위
TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩입니다.

## 남은 약점
- 제공 trace가 minimal synthetic capture라 일부 certificate detail과 extension은 제한적입니다.
- decryption 실습은 필수 범위에 넣지 않았습니다.
