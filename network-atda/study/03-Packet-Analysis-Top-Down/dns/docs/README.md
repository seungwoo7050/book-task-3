# 개념 문서 안내

## 이 폴더의 역할
이 디렉터리는 `DNS Packet Analysis`를 공부할 때 반복해서 다시 볼 개념과 판단 근거만 남깁니다. 문제 이해의 출발점은 아니며, `problem/README.md`와 `analysis/README.md`를 읽은 뒤 필요한 문서만 다시 참조합니다.

## 먼저 볼 파일
- [`dns-hierarchy.md`](concepts/dns-hierarchy.md)
- [`dns-protocol.md`](concepts/dns-protocol.md)

## 기준 명령
- 기준 검증: `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`
- 개념 문서 위치: `docs/concepts/`
- 참고 자료 위치: `docs/references/`

## 현재 범위
- DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩입니다.

## 남은 약점
- 이 폴더만으로 문제와 답을 모두 이해할 수 있게 만들지 않습니다.
- 최신 공개 범위와 한계는 프로젝트 README를 기준으로 확인합니다.
