# Wi-Fi 보안 프로토콜의 진화: WEP → WPA → WPA2 → WPA3

## 개요

IEEE 802.11 무선 LAN은 공유 무선 매체를 사용하므로 도청이 용이하며,
이를 보호하기 위한 보안 프로토콜이 WEP에서 WPA3까지 진화해왔다.
이 문서는 각 보안 프로토콜의 구조, 취약점, 개선 사항을 분석하고
Wireshark 실습의 비콘/인증 프레임 관찰과 연결한다.

---

## 1. WEP (Wired Equivalent Privacy, 1997)

### 동작 원리

```
평문 + ICV(CRC-32) 연결
→ RC4(IV || Key) 스트림으로 XOR 암호화
→ [IV(24bit) | KeyID(2bit)] || 암호문 || ICV
```

### 핵심 취약점

| 취약점 | 설명 |
| :--- | :--- |
| IV 재사용 | 24비트 IV → 약 5000 패킷 후 충돌 (Birthday Paradox) |
| RC4 약한 키 | 특정 IV 패턴에서 키 바이트 노출 (FMS 공격) |
| CRC-32 무결성 | 암호학적 해시가 아님 → 비트 플립 공격 가능 |
| 정적 키 | 모든 사용자가 동일한 공유 키 사용 |

### 공격 도구

- **aircrack-ng**: 충분한 IV를 수집하면 수 분 내 키 복구 가능
- 현재는 **완전히 폐기**된 프로토콜

---

## 2. WPA (Wi-Fi Protected Access, 2003)

### TKIP (Temporal Key Integrity Protocol)

WEP 하드웨어에서 펌웨어 업그레이드만으로 적용 가능하도록 설계되었다.

```
개선점:
- 48비트 IV (IV 재사용 문제 완화)
- Per-Packet Key Mixing (패킷별 고유 키 생성)
- Michael MIC (Message Integrity Check) 추가
- IV Sequencing (재전송 공격 방지)
```

### WPA-Personal (PSK)

```
Pre-Shared Key (비밀번호)
→ PBKDF2(SSID, passphrase, 4096) → PMK (Pairwise Master Key)
→ 4-Way Handshake → PTK (Pairwise Transient Key)
```

### WPA-Enterprise (802.1X/EAP)

```
스테이션 ↔ AP ↔ RADIUS 서버
EAP 인증 → PMK 생성 → 4-Way Handshake → PTK
```

### 한계

- TKIP는 RC4 기반 → 근본적 보안 취약점 존재
- Michael MIC의 약점 (Beck-Tews 공격, 2008)

---

## 3. WPA2 (802.11i, 2004)

### CCMP (Counter Mode with CBC-MAC Protocol)

```
AES-128-CCM:
- Counter Mode (CTR): 기밀성 제공
- CBC-MAC: 무결성 + 인증 제공
→ AEAD (Authenticated Encryption with Associated Data)
```

### 4-Way Handshake

```
AP                                     Station
──                                     ───────
Message 1: ANonce            ──────→
                             ←──────   Message 2: SNonce + MIC
                                       (Station이 PTK 계산)
Message 3: GTK + MIC        ──────→
(AP가 PTK 계산 확인)
                             ←──────   Message 4: ACK
```

- **PTK 도출**: PMK + ANonce + SNonce + AP MAC + Station MAC → PRF → PTK
- **GTK**: 브로드캐스트/멀티캐스트 트래픽 암호화용 그룹 키

### KRACK 공격 (2017)

4-Way Handshake의 Message 3 재전송을 악용하여 Nonce를 리셋시킨다:

```
공격자가 Message 3를 가로채고 재전송
→ Station이 이미 설치된 키를 재설치
→ Nonce 카운터 리셋 → 키스트림 재사용 → 평문 복호화 가능
```

패치: Message 3 재수신 시 Nonce 리셋 방지.

### Wireshark에서 관찰

비콘 프레임의 RSN Information Element에서 WPA2 설정 확인:
- **Group Cipher Suite**: CCMP (AES)
- **Pairwise Cipher Suite**: CCMP
- **AKM Suite**: PSK 또는 802.1X

---

## 4. WPA3 (2018)

### SAE (Simultaneous Authentication of Equals)

WPA2-PSK의 4-Way Handshake 대신 **Dragonfly Key Exchange** 사용:

```
기존 WPA2-PSK:
  비밀번호 → PBKDF2 → PMK → 4-Way Handshake
  → 오프라인 사전 공격 가능 (캡처한 핸드셰이크로)

WPA3-SAE:
  비밀번호 → Commit/Confirm 교환 → PMK
  → 오프라인 사전 공격 불가 (각 추측에 AP 참여 필요)
```

### 주요 개선

| 항목 | WPA2 | WPA3 |
| :--- | :--- | :--- |
| 키 교환 | PSK + 4-Way | SAE (Dragonfly) |
| 오프라인 사전 공격 | 취약 | 방어됨 |
| Forward Secrecy | 미제공 | 제공 |
| 개방 네트워크 보호 | 없음 | OWE (Opportunistic Wireless Encryption) |
| 관리 프레임 보호 | 선택적 (PMF) | 필수 (PMF) |

### OWE (Opportunistic Wireless Encryption)

공개 Wi-Fi에서도 인증 없이 암호화된 통신을 제공:

```
기존: 공개 Wi-Fi = 평문 통신 → 도청 가능
OWE: DH 키 교환으로 암호화 → 도청 방지 (인증은 미제공)
```

---

## 5. 보안 프로토콜 비교 요약

| 항목 | WEP | WPA | WPA2 | WPA3 |
| :--- | :--- | :--- | :--- | :--- |
| 암호 알고리즘 | RC4 | RC4 (TKIP) | AES (CCMP) | AES (CCMP/GCMP) |
| IV 길이 | 24비트 | 48비트 | 48비트 | — |
| 무결성 | CRC-32 | Michael MIC | CBC-MAC | GMAC/CBC-MAC |
| 키 교환 | 정적 | 4-Way | 4-Way | SAE |
| Forward Secrecy | X | X | X | O |
| 현재 상태 | 폐기 | 지원 종료 예정 | 현역 | 신규 권장 |

---

## 6. 실습과의 연결

802.11 Wireshark 실습에서 관찰한 내용과 보안의 관계:

1. **비콘 프레임의 RSN IE**: WPA2/WPA3의 암호 스위트 및 AKM 정보 확인
2. **인증 프레임**: Open System 인증 후 4-Way Handshake로 키 협상 시작
3. **Association Request/Response**: 스테이션과 AP의 보안 능력 협상
4. **Management 프레임 평문 문제**: WPA3의 PMF(Protected Management Frames)로 해결
5. **프레임 암호화 여부**: Data 프레임의 Protected 비트(Frame Control)로 암호화 상태 확인
