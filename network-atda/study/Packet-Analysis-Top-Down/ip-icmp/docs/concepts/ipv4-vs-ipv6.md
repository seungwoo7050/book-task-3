# IPv4 vs IPv6 전환과 네트워크 계층의 진화

## 개요

IPv4는 4.3×10⁹개의 주소 공간을 제공하지만 이미 고갈되었다.
IPv6는 이 문제를 해결하면서 헤더 구조를 단순화하고, 단편화 처리를 변경하며,
보안(IPsec)을 내장하는 등 근본적인 설계 개선을 도입했다.
이 문서는 IP/ICMP Wireshark 실습과 연결하여 두 프로토콜의 차이를 분석한다.

---

## 1. 헤더 구조 비교

### IPv4 헤더 (20–60 bytes)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (variable)                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### IPv6 헤더 (고정 40 bytes)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version| Traffic Class |           Flow Label                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Payload Length        |  Next Header  |   Hop Limit   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                                                               +
|                       Source Address (128 bits)                |
+                                                               +
|                                                               |
+                                                               +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                                                               +
|                    Destination Address (128 bits)              |
+                                                               +
|                                                               |
+                                                               +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 필드 대응 관계

| IPv4 필드 | IPv6 대응 | 변경사항 |
| :--- | :--- | :--- |
| Version (4) | Version (6) | 값만 변경 |
| IHL | 제거됨 | 고정 헤더이므로 불필요 |
| Total Length | Payload Length | 헤더 제외한 페이로드 길이만 |
| Identification, Flags, Fragment Offset | 제거됨 | 확장 헤더로 이동 |
| TTL | Hop Limit | 이름만 변경, 동일 기능 |
| Protocol | Next Header | 확장 헤더 체인 지원 |
| Header Checksum | 제거됨 | 하위/상위 계층에 위임 |
| Options | 확장 헤더(Extension Headers) | 체인 구조로 유연성 증가 |

---

## 2. 단편화 처리의 차이

### IPv4 단편화

- **중간 라우터**가 MTU 초과 시 단편화 수행 가능
- Identification, MF 플래그, Fragment Offset으로 제어
- 실습에서 관찰: 대형 ICMP 페이로드 전송 시 단편화 발생

### IPv6 단편화

- **중간 라우터는 단편화하지 않음** (Drop + ICMPv6 Packet Too Big)
- **송신 호스트만** 단편화 수행 (Fragment Extension Header 사용)
- **Path MTU Discovery (PMTUD)** 가 필수적

### 설계 철학

```
IPv4: 라우터도 단편화 가능 → 라우터 부담 증가
IPv6: 송신자만 단편화 → 라우터 처리 단순화, 성능 향상
```

---

## 3. ICMPv4 vs ICMPv6

### 공통 기능

| 기능 | ICMPv4 Type | ICMPv6 Type |
| :--- | :--- | :--- |
| Echo Request | 8 | 128 |
| Echo Reply | 0 | 129 |
| Destination Unreachable | 3 | 1 |
| Time Exceeded | 11 | 3 |
| Parameter Problem | 12 | 4 |

### ICMPv6 추가 기능

ICMPv6는 IPv4에서 별도 프로토콜이던 기능들을 통합한다:

| 기능 | IPv4 | IPv6 |
| :--- | :--- | :--- |
| 주소 해석 | ARP (별도 프로토콜) | NDP (ICMPv6 Type 135/136) |
| 라우터 발견 | IGMP | ICMPv6 Router Solicitation/Advertisement |
| 멀티캐스트 관리 | IGMP | MLD (ICMPv6 기반) |
| Packet Too Big | ICMP Type 3 Code 4 | ICMPv6 Type 2 |

---

## 4. 전환 메커니즘

### Dual Stack

- 호스트가 IPv4와 IPv6 스택을 동시에 운영
- DNS 응답에 따라 A(IPv4) 또는 AAAA(IPv6) 레코드 선택
- 가장 일반적인 전환 방법

### 터널링 (Tunneling)

- IPv6 패킷을 IPv4 패킷 내에 캡슐화하여 전송
- 6to4, ISATAP, Teredo 등의 기법
- IPv4 전용 네트워크 구간 횡단에 사용

### NAT64/DNS64

- IPv6 전용 호스트가 IPv4 서버에 접근
- DNS64: IPv4 주소를 IPv6 주소로 합성
- NAT64: IPv6↔IPv4 패킷 변환

---

## 5. 주소 공간 비교

| 속성 | IPv4 | IPv6 |
| :--- | :--- | :--- |
| 주소 길이 | 32비트 | 128비트 |
| 주소 수 | ~4.3 × 10⁹ | ~3.4 × 10³⁸ |
| 표기법 | 점으로 구분된 10진수 (192.168.1.1) | 콜론으로 구분된 16진수 (2001:db8::1) |
| NAT 의존도 | 높음 (주소 부족) | 낮음 (종단 간 통신 가능) |
| DHCP | DHCPv4 | SLAAC + DHCPv6 |

---

## 6. 실습과의 연결

IP/ICMP Wireshark 실습에서 관찰한 내용과 IPv6의 관계:

1. **IPv4 헤더 필드 분석**: IPv6에서 제거되거나 변경된 필드들의 이유 이해
2. **TTL → Hop Limit**: 동일한 루프 방지 메커니즘, 이름만 변경
3. **IP 단편화 관찰**: IPv6에서는 라우터가 수행하지 않으므로 PMTUD 필수
4. **ICMP 메시지 분석**: ICMPv6에서 Type 번호가 변경되고 ARP/IGMP 기능 통합
5. **traceroute**: IPv6 환경에서도 동일한 원리(Hop Limit 활용)로 동작
