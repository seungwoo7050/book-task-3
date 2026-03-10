# DNS Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 DNS Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/dns/problem test` |

## 한 줄 요약

DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩입니다.

## 왜 이 프로젝트가 필요한가

HTTP 다음 단계에서 이름 해석 계층을 관찰하며, 패킷 분석이 응용 계층 내부 프로토콜에도 그대로 적용된다는 점을 보여 줍니다.

## 이런 학습자에게 맞습니다

- DNS record type과 recursive resolution을 trace로 이해하고 싶은 학습자
- 브라우저 트래픽에서 DNS가 어떤 흔적을 남기는지 보고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 질문 목록과 trace 범위를 먼저 확인합니다.
2. `analysis/README.md` - 공개 답안이 어떤 evidence 원칙으로 작성되는지 확인합니다.
3. `docs/README.md` - 개념 문서 중 지금 필요한 부분만 다시 읽습니다.

## 제공 자료

- `problem/data/dns-nslookup.pcapng`: `nslookup`/`dig` 계열 질의 trace
- `problem/data/dns-web-browsing.pcapng`: 웹 브라우징 중 발생한 DNS trace
- `analysis/src/dns-analysis.md`: 공개 답안

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/dns/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 학습 포인트

- DNS header/question/answer 구조
- record type별 역할
- recursive resolution과 authoritative/non-authoritative 차이
- TTL 감소와 cache hit 해석

## 현재 한계

- 제공된 trace가 짧아 일부 질문은 관찰 불가로 남습니다.
- 권한 서버 위임 체인을 완전히 재현하는 trace는 아닙니다.
- 일부 응답은 malformed 상태라 field 해석이 제한됩니다.

## 포트폴리오로 확장하기

- 동일한 질문을 로컬 `dig` 캡처나 다른 사이트 trace에 적용해 보면 학습 결과가 더 풍부해집니다.
- record type별 의미를 표로 정리하면 나중에 다시 볼 때 큰 도움이 됩니다.
- 웹 브라우징 trace와 `nslookup` trace를 비교한 메모를 추가하면 단순 답안집과 달라집니다.
