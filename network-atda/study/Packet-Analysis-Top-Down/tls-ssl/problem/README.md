# Problem: TLS/SSL Analysis

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Trace Files

- `tls-trace.pcap` — Pre-captured HTTPS session including full TLS handshake(s), certificate exchange, and encrypted data transfer

> Download from the textbook companion site or capture your own by visiting an HTTPS website while running Wireshark.

---

## Part 1: ClientHello (Q1–Q5)

Examine the ClientHello message sent by the client at the start of the TLS handshake.

**Q1.** What is the TLS record content type for the ClientHello message? What is the TLS version indicated in the record layer vs. the handshake layer?

**Q2.** What cipher suites does the client advertise in the ClientHello? List the number of cipher suites and identify at least 3 specific ones by name.

**Q3.** Does the ClientHello include a Server Name Indication (SNI) extension? If so, what server name is specified?

**Q4.** What TLS versions does the client indicate it supports? (Examine the "supported_versions" extension if present, or the handshake version field.)

**Q5.** What other notable extensions are present in the ClientHello? Identify at least 3 extensions and briefly describe their purpose.

---

## Part 2: ServerHello and Certificate (Q6–Q11)

Examine the ServerHello message and the server's certificate.

**Q6.** What cipher suite did the server select in the ServerHello? What does each component of the cipher suite name mean?

**Q7.** What TLS version was ultimately negotiated for this session? Where is this indicated?

**Q8.** Examine the server's Certificate message. How many certificates are in the certificate chain? What is the subject (Common Name) of each certificate?

**Q9.** What is the issuer of the server's (leaf) certificate? Is the root CA certificate included in the chain sent by the server?

**Q10.** What is the validity period (Not Before / Not After) of the server's certificate? What signature algorithm was used to sign it?

**Q11.** Does the ServerHello or subsequent messages include a ServerKeyExchange message? If so, what key exchange parameters are provided?

---

## Part 3: Handshake Completion (Q12–Q16)

Analyze the remaining handshake messages and the transition to encrypted communication.

**Q12.** Identify the ChangeCipherSpec message(s) in the trace. How many are there and who sends them (client, server, or both)?

**Q13.** After the ChangeCipherSpec, what is the next message sent? Can you read its contents? Why or why not?

**Q14.** What is the complete sequence of TLS handshake messages exchanged? List them in order with frame numbers and the sender (client/server).

**Q15.** How many TCP segments (round trips) does the TLS handshake require before application data can be sent? Count from the first ClientHello to the first Application Data record.

**Q16.** If this is a TLS 1.3 session, how does the handshake differ from TLS 1.2? Identify specific differences in the message flow you observe.

---

## Part 4: Application Data and Record Protocol (Q17–Q20)

Examine TLS records carrying encrypted application data.

**Q17.** Find an Application Data record. What is the TLS record content type value? What is the length of the encrypted payload?

**Q18.** Can you determine what application protocol (e.g., HTTP) is being carried inside the TLS records without decryption? What information (if any) leaked in plaintext during the handshake reveals the application purpose?

**Q19.** Examine the TLS record headers of several Application Data messages. Are the record lengths uniform or variable? What is the maximum TLS record size you observe?

**Q20.** If you have a pre-master secret log file (SSLKEYLOGFILE), configure Wireshark to decrypt the session. What HTTP request and response are visible after decryption?

---

## Total: 20 Questions
