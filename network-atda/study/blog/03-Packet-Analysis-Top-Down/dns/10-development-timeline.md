# DNS Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 DNS 전체를 백과사전처럼 설명하는 식이 아니다. 오히려 trace가 너무 짧기 때문에, 먼저 말할 수 있는 범위를 좁히고 그 안에서 query/response 구조를 층층이 확정하는 순서로 전개된다. 코드가 아니라 answer markdown 기준 전환점은 네 번이다.

## 1. 먼저 `nslookup` trace에서 query와 response의 최소 쌍을 고정한다

출발점은 `dns-nslookup.pcapng` 4패킷이다. `filter-queries` 재실행 결과 frame `1`, `3`이 모두 `8.8.8.8`로 향하고, type은 각각 `A (1)`, `MX (15)`였다. answer markdown도 이 두 query를 기준선으로 잡아 `Answer RRs: 0`인 request와 response를 분리한다.

이 첫 단계 덕분에 이 lab는 "DNS는 보통 UDP 53을 쓴다" 같은 일반 설명이 아니라, 실제 trace의 `udp.dstport=53`와 `ip.dst=8.8.8.8`에서 출발한다.

## 2. A query는 깔끔하게 끝나지만 MX query는 decode 한계에서 멈춘다

frame `2`는 정리하기 쉽다. `example.com A 93.184.216.34 TTL 300`이 명확하게 보인다. 하지만 frame `4`는 `Type: MX`와 `TTL 300`까지만 안정적으로 확인되고, answer detail은 malformed로 끊긴다. 현재 답안이 MX host/preference를 빈칸으로 남기는 이유가 여기 있다.

중요한 건 이 빈칸을 약점으로 숨기지 않는 것이다. trace에서 안 보이는 값을 상식으로 메우면 이 lab의 목적이 무너진다.

## 3. authoritative 여부는 flag로 보지만 delegation chain은 보지 못한다

답안은 frame `2`의 `Authoritative: 1`, frame `4`의 `Authoritative: 0`을 대비해 authoritative와 non-authoritative 차이를 설명한다. 하지만 추가 record가 비어 있기 때문에 authoritative nameserver IP까지는 이어지지 않는다. 즉 이 단계에서 얻는 것은 "누가 최종 답을 말하고 있는가"의 구분이지, 전체 DNS hierarchy 복원은 아니다.

이런 식으로 flag interpretation과 zone delegation을 구분하는 태도가 이 lab의 핵심 학습 포인트 중 하나다.

## 4. web browsing trace는 DNS가 짧은 전처리 단계라는 사실만 보여 준다

`dns-web-browsing.pcapng`는 단 2패킷이다. frame `1`은 `1.1.1.1`로 향하는 `www.ietf.org` query, frame `2`는 response다. answer markdown는 여기서 CNAME 하나를 decode하고, follow-up TCP SYN이나 TTL 감소는 `Not observable`로 남긴다.

즉 이 lab의 마지막 전환점은 "DNS는 보통 더 긴 browsing chain의 일부지만, 현재 trace는 그 일부만 담고 있다"는 경계 인식이다. 이 절제가 문서 품질을 올려 준다.

## 지금 남는 한계

현재 증거는 의도적으로 작다. `nslookup` trace는 4패킷, browsing trace는 2패킷뿐이라 cache reuse, recursive delegation, transport follow-up을 추적할 수 없다. 그래서 이 lab는 DNS 전체를 닫는 문서가 아니라, 짧은 trace에서 query/response 읽기 원칙을 훈련하는 문서로 읽는 편이 정확하다.
