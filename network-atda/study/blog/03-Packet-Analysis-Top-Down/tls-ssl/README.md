# TLS Packet Analysis Blog

이 문서 묶음은 `tls-ssl` 랩을 "TLS가 안전하다"는 설명보다 "암호화가 시작되기 전후에 trace가 어떤 정보는 드러내고 어떤 정보는 감춘다는 사실을 어디서 확인하는가"라는 질문으로 다시 읽는다. 현재 공개 답안은 6-frame synthetic trace에서 `ClientHello`, `ServerHello + Certificate`, `ChangeCipherSpec + Application Data`를 읽고, cipher suite ID와 version field는 확인하되 certificate 세부나 plaintext application message는 끝까지 복원하지 않는다. 따라서 이 lab의 핵심은 TLS를 다 안다는 착각보다, handshake visibility와 post-encryption opacity가 어디서 갈리는지 정확히 보는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/tls-ssl/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/tls-ssl-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`
- 보조 필터: `make -C .../tls-ssl/problem client-hello`, `server-hello`, `app-data`, `records`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`
- 결과: `PASS: tls-ssl answer file passed content verification`
- 보조 필터에서 재확인한 값:
  - ClientHello: frame `4`, version `0x0303`, cipher suites `0x1301,0x1302`
  - ServerHello: frame `5`, selected cipher `0x1301`
  - Application Data: frame `6`, record lengths `1,32`
- 현재 환경 주의: `make certs`는 `docs/concepts/wireshark-tls.md`가 예시로 드는 `x509sat.utf8String` field를 이 `tshark` build가 제공하지 않아 실패했다. 이번 검증에서 `tshark -G fields | rg x509`를 다시 확인했을 때는 `x509af.*` 계열만 노출됐다.

## 지금 남기는 한계

- trace가 6 frame뿐이라 full canonical TLS 1.2/1.3 handshake를 다 보여 주지 않는다.
- certificate record는 malformed로 표시돼 issuer/subject 세부를 안정적으로 decode할 수 없다.
- decrypt key material이 없어 application plaintext는 볼 수 없다.
