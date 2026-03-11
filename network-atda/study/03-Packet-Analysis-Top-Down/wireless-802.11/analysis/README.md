# 공개 답안 안내

## 이 폴더의 역할
이 디렉터리는 `802.11 Wireless Packet Analysis`의 공개 답안과 핵심 근거 문서를 담습니다. 프로젝트 README에서 문제를 확인한 뒤, 실제 답은 여기서 읽습니다.

## 먼저 볼 파일
- `analysis/src/wireless-analysis.md` - 질문별 답안과 근거를 확인합니다.

## 기준 명령
- 검증: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`

## 현재 범위
비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩입니다.

## 남은 약점
- compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있습니다.
- EAPOL/WPA handshake 심화는 포함하지 않습니다.
- 실제 RF 잡음과 retry 패턴은 제한적으로만 보입니다.
