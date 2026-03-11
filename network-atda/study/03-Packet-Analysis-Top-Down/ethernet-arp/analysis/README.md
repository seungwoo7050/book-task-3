# 공개 답안 안내

## 이 폴더의 역할
이 디렉터리는 `Ethernet and ARP Packet Analysis`의 공개 답안과 핵심 근거 문서를 담습니다. 프로젝트 README에서 문제를 확인한 뒤, 실제 답은 여기서 읽습니다.

## 먼저 볼 파일
- `analysis/src/ethernet-arp-analysis.md` - 질문별 답안과 근거를 확인합니다.

## 기준 명령
- 검증: `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`

## 현재 범위
링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩입니다.

## 남은 약점
- trace가 작아 교재의 일부 확장 질문은 관찰 불가입니다.
- Gratuitous ARP나 ARP spoofing 사례는 포함하지 않습니다.
