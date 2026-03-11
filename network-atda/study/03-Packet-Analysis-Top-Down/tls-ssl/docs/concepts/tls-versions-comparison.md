# TLS 1.2 vs TLS 1.3 비교 분석과 보안 진화

## 개요

TLS 1.3 (RFC 8446, 2018)은 TLS 1.2 대비 보안성과 성능을 동시에 개선했다.
이 문서는 두 버전의 핸드셰이크 차이, 제거된 기능, 새로운 보안 특성을
Wireshark 실습에서 관찰한 내용과 연결하여 분석한다.

---

## 1. 핸드셰이크 비교

### TLS 1.2 핸드셰이크 (2-RTT)

```
Client                                  Server
──────                                  ──────
ClientHello            ──────────→
                       ←──────────      ServerHello
                       ←──────────      Certificate
                       ←──────────      ServerKeyExchange
                       ←──────────      ServerHelloDone
ClientKeyExchange      ──────────→
ChangeCipherSpec       ──────────→
Finished               ──────────→
                       ←──────────      ChangeCipherSpec
                       ←──────────      Finished
Application Data       ←────────→      Application Data
```

**총 2 RTT** 후 애플리케이션 데이터 전송 시작.

### TLS 1.3 핸드셰이크 (1-RTT)

```
Client                                  Server
──────                                  ──────
ClientHello            ──────────→
  + key_share                           
  + supported_versions
                       ←──────────      ServerHello
                                          + key_share
                       ←──────────      {EncryptedExtensions}
                       ←──────────      {Certificate}
                       ←──────────      {CertificateVerify}
                       ←──────────      {Finished}
{Finished}             ──────────→
Application Data       ←────────→      Application Data
```

**총 1 RTT** 후 애플리케이션 데이터 전송 시작.
`{}` = 암호화된 메시지.

### 핸드셰이크 차이 요약

| 항목 | TLS 1.2 | TLS 1.3 |
| :--- | :--- | :--- |
| RTT 수 | 2 RTT | 1 RTT (0-RTT 가능) |
| 키 교환 시점 | ClientKeyExchange | ClientHello의 key_share 확장 |
| 서버 인증서 암호화 | 평문 전송 | 암호화 후 전송 |
| ChangeCipherSpec | 필수 | 호환성 목적의 더미만 (선택적) |
| 최초 암호화 시점 | Finished 메시지부터 | ServerHello 직후부터 |

---

## 2. 제거된 기능 (TLS 1.3)

### 제거된 암호 스위트 구성 요소

| 제거 항목 | 이유 |
| :--- | :--- |
| RSA 키 교환 | Forward Secrecy 미제공 |
| DH (정적) 키 교환 | Forward Secrecy 미제공 |
| CBC 모드 암호 | BEAST, Lucky 13 등 패딩 오라클 공격 취약 |
| RC4 스트림 암호 | 통계적 편향 공격 |
| SHA-1 해시 | 충돌 공격 가능 |
| DES/3DES 암호 | 짧은 블록 크기(64비트), Sweet32 공격 |

### TLS 1.3 허용 암호 스위트

```
TLS_AES_256_GCM_SHA384
TLS_AES_128_GCM_SHA256
TLS_CHACHA20_POLY1305_SHA256
TLS_AES_128_CCM_SHA256
TLS_AES_128_CCM_8_SHA256
```

**모두 AEAD(Authenticated Encryption with Associated Data)** 만 허용.

---

## 3. Forward Secrecy (전방 비밀성)

### 정의

서버의 장기 비밀키가 유출되어도 과거의 세션 키를 복구할 수 없는 속성.

### TLS 1.2에서의 문제

RSA 키 교환 사용 시:
```
Pre-Master Secret = RSA_Encrypt(server_public_key, random)
→ 서버 개인키 유출 시 모든 과거 세션의 Pre-Master Secret 복호화 가능
```

### TLS 1.3에서의 해결

**모든 키 교환이 일시적(ephemeral) Diffie-Hellman**:
```
각 세션마다 새로운 DH 키 쌍 생성
→ 세션 키 = DH(client_ephemeral, server_ephemeral)
→ 서버 장기 키 유출 시에도 과거 세션 키 복구 불가
```

---

## 4. 0-RTT (Early Data)

### 동작 원리

이전 연결에서 공유한 PSK(Pre-Shared Key)를 활용하여
핸드셰이크 완료 전에 애플리케이션 데이터를 전송한다:

```
Client                                  Server
──────                                  ──────
ClientHello            ──────────→
  + early_data
  + key_share
  + psk_key_exchange_modes
  + pre_shared_key
(Application Data)     ──────────→      ← 0-RTT 데이터
                       ←──────────      ServerHello
                                          + pre_shared_key
                       ←──────────      {EncryptedExtensions}
                       ←──────────      {Finished}
{EndOfEarlyData}       ──────────→
{Finished}             ──────────→
```

### 보안 주의사항

| 위험 | 설명 |
| :--- | :--- |
| Replay Attack | 0-RTT 데이터는 재전송 공격에 취약 |
| Forward Secrecy 미제공 | PSK 기반이므로 DH 키 교환 이전 |
| 비멱등 요청 금지 | POST 등 부작용 있는 요청은 0-RTT로 전송 부적절 |

---

## 5. 인증서 관련 변경

### TLS 1.2

- Certificate 메시지가 평문으로 전송됨
- 서버의 인증서 체인이 도청자에게 노출
- SNI(Server Name Indication)도 평문

### TLS 1.3

- Certificate 메시지가 핸드셰이크 키로 암호화
- CertificateVerify 메시지 추가: 서버가 개인키 소유를 명시적으로 증명
- **ECH(Encrypted Client Hello)** (진행 중): SNI까지 암호화하려는 노력

### Wireshark에서의 차이

```
TLS 1.2: Certificate 메시지 내용을 직접 확인 가능
TLS 1.3: Certificate가 암호화되어 있어 복호화 키 없이는 확인 불가
```

---

## 6. Record Protocol 변경

### TLS 1.2 레코드

```
ContentType(1) | Version(2) | Length(2) | Fragment
```

- ContentType: Handshake(22), Application Data(23), ChangeCipherSpec(20), Alert(21)

### TLS 1.3 레코드

```
ContentType(1) | Legacy Version(2) | Length(2) | Encrypted Fragment
  → 실제 ContentType은 암호화된 페이로드 내부에 포함
```

- 외부 ContentType은 항상 Application Data(23)로 설정 (미들박스 호환성)
- 실제 ContentType은 복호화 후에만 확인 가능

---

## 7. 실습과의 연결

TLS/SSL Wireshark 실습 관찰 사항과의 연결:

1. **ClientHello 분석**: 지원 암호 스위트 목록에서 TLS 1.3 전용 AEAD 스위트 식별
2. **ServerHello 분석**: 선택된 버전(supported_versions 확장)으로 1.2/1.3 구분
3. **Certificate 가시성**: TLS 1.2에서는 인증서 체인 확인 가능, 1.3에서는 암호화
4. **핸드셰이크 RTT**: 메시지 타임스탬프로 1-RTT vs 2-RTT 확인
5. **ChangeCipherSpec 유무**: TLS 1.3에서의 더미 CCS 메시지 관찰 (호환성)
