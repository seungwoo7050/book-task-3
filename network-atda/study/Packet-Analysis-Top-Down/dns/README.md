# DNS Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/dns` |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/dns/problem test` |

## 한 줄 요약

DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩이다.

## 문제 요약

A, AAAA, CNAME, MX, NS 같은 DNS record type과 recursive query 맥락을 제공된 trace에서 읽어낸다.

## 이 프로젝트를 여기 둔 이유

HTTP 다음 단계에서 이름 해석 계층을 관찰하며, 패킷 분석이 응용 계층 내부 프로토콜에도 적용된다는 점을 보여준다.

## 제공 자료

- `problem/data/dns-nslookup.pcapng`
- `problem/data/dns-web-browsing.pcapng`
- `analysis/src/dns-analysis.md`

## 학습 포인트

- DNS header/question/answer 구조
- record type별 역할
- recursive resolution 개념
- TTL 감소와 cache hit 해석

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/dns/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 범위와 한계

제공된 trace가 짧기 때문에 일부 질문은 not observable로 남는다.

- 현재 한계: 권한 서버 위임 체인을 완전하게 보여주는 trace가 아님
- 현재 한계: Malformed MX 응답이 일부 필드를 가린다

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
