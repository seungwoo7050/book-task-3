# 공개 답안 안내

## 이 폴더의 역할
이 디렉터리는 `DNS Packet Analysis`의 공개 답안과 핵심 근거 문서를 담습니다. 프로젝트 README에서 문제를 확인한 뒤, 실제 답은 여기서 읽습니다.

## 먼저 볼 파일
- `analysis/src/dns-analysis.md` - 질문별 답안과 근거를 확인합니다.

## 기준 명령
- 검증: `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`

## 현재 범위
DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩입니다.

## 남은 약점
- 제공된 trace가 짧아 일부 질문은 관찰 불가로 남습니다.
- 권한 서버 위임 체인을 완전히 재현하는 trace는 아닙니다.
- 일부 응답은 malformed 상태라 field 해석이 제한됩니다.
