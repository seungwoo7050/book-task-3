# Problem: 802.11 Wireless Analysis

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Trace Files

- `wireless-trace.pcap` — Pre-captured 802.11 wireless traffic including beacon frames, probe requests, association, and data transfer (monitor mode capture)

> Download from the textbook companion site or capture your own using a wireless adapter in monitor mode.

---

## Part 1: Beacon Frames (Q1–Q5)

Examine beacon frames broadcast by access points in the trace.

**Q1.** What are the SSIDs of the access points that are issuing most of the beacon frames in the trace? List all unique SSIDs you observe.

**Q2.** What is the interval of time between successive beacon frames from one AP? (Examine the beacon interval field and verify with timestamps.)

**Q3.** What is the source MAC address in the beacon frame for one of the identified APs? Is this address also the BSS ID?

**Q4.** The beacon frame contains information about supported rates. What are the supported rates and extended supported rates advertised by one of the APs?

**Q5.** What is the capability information advertised in the beacon frame? Does the AP support WEP/WPA/WPA2 encryption? Identify the specific security information elements.

---

## Part 2: Probe Request and Response (Q6–Q9)

Analyze probe request and probe response frames in the trace.

**Q6.** Find a probe request frame. What is the source MAC address and SSID (if any) in the probe request?

**Q7.** Find the corresponding probe response frame. What is the source MAC address in the probe response? Is it from the same AP whose beacon frames you examined?

**Q8.** Compare the information elements in the probe response with those in a beacon frame from the same AP. Are they identical? What differences (if any) do you observe?

**Q9.** What is the destination MAC address in the probe request frame? Why is this address used?

---

## Part 3: Authentication and Association (Q10–Q14)

Trace the authentication and association exchange between a wireless station and an AP.

**Q10.** Find an Authentication frame. What is the authentication algorithm used (Open System or Shared Key)?

**Q11.** What are the source and destination MAC addresses in the Authentication request frame? What is the authentication status code in the Authentication response?

**Q12.** Find the Association Request frame following successful authentication. What information does the station provide to the AP in this frame?

**Q13.** What is the Association Response status code? What is the Association ID (AID) assigned to the station by the AP?

**Q14.** Summarize the complete sequence of management frames exchanged from initial probe to successful association. List the frame types in order with their frame numbers.

---

## Part 4: Data Frames and Frame Structure (Q15–Q18)

Examine 802.11 data frames and the general frame structure.

**Q15.** Find an 802.11 data frame. How many MAC address fields are present in the header? What are their roles (source, destination, BSSID, etc.) based on the To DS and From DS bits?

**Q16.** What is the value of the Frame Control field's Type and Subtype for a data frame? What about for a beacon frame and an ACK frame?

**Q17.** Examine the Duration/ID field in a data frame. What value does it contain and what does it represent?

**Q18.** Find an 802.11 ACK (Acknowledgment) control frame. How many address fields does it contain? What is the relationship between this ACK and the preceding data frame?

---

## Total: 18 Questions
