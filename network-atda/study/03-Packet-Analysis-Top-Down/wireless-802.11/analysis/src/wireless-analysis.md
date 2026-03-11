# 802.11 Wireless — Solution

## Trace Limitations

- This report uses only the repository-provided trace file.
- If a worksheet item needs packets that are not present in this trace, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.

Trace used: `wireless-trace.pcap` (10 frames).

Because this is a compact synthetic trace, several management/data details are simplified compared with real monitor-mode captures.

## Part 1: Beacon Frames (Q1–Q5)

### Q1. SSIDs of Access Points Issuing Beacon Frames

Unique SSIDs observed in beacon frames:
- **30 Munroe St** (frame #1)
- **linksys12** (frame #2)

### Q2. Beacon Interval

Beacon interval field is **100 TU** in both beacons (frames #1 and #2), i.e.:
- `100 * 1024 us = 102400 us = 102.4 ms`

Timestamp-based same-AP interval verification is not possible here because each AP appears with only one beacon frame in this trace.

### Q3. Source MAC Address and BSSID

For SSID `30 Munroe St` (frame #1):
- Source/Transmitter MAC: **00:16:b6:f7:1d:51**
- BSSID: **00:16:b6:f7:1d:51**

Yes, they are the same.

### Q4. Supported Rates / Extended Supported Rates

From beacon frame #1 (`30 Munroe St`):
- Supported rates: **1(B), 2(B), 5.5(B), 11(B), 6, 9, 12, 18 Mbps**
- Extended Supported Rates tag is not present in this frame.

From beacon frame #2 (`linksys12`):
- Supported rates: **1(B), 2(B), 5.5(B), 11(B)**

### Q5. Capability Info and Security

Frame #1 capability info is **0x0011**:
- ESS = 1
- Privacy = 1

No RSN/WPA/WPA2 information element is decoded in this trace. So we can confirm privacy-required signaling, but not explicit WPA/WPA2 AKM/cipher suite details from tagged RSN/WPA IEs.

---

## Part 2: Probe Request and Response (Q6–Q9)

### Q6. Probe Request Source and SSID

Probe Request is frame **#3**:
- Source MAC: **00:12:f0:1c:3e:82**
- SSID: **30 Munroe St**

### Q7. Probe Response Source

Probe Response is frame **#4**:
- Source MAC: **00:16:b6:f7:1d:51**

Yes, this is the same AP as beacon frame #1.

### Q8. Probe Response vs Beacon Comparison

Comparing frame #4 (probe response) with frame #1 (beacon):
- Common: same SSID (`30 Munroe St`), same AP MAC/BSSID, same beacon interval field value (100 TU)
- Differences in this trace: capability bits differ (`0x0000` vs `0x0011`), and frame #4 carries fewer tagged parameters than the beacon.

### Q9. Probe Request Destination MAC and Reason

Probe request destination is **ff:ff:ff:ff:ff:ff** (broadcast) in frame #3, so nearby APs can respond.

---

## Part 3: Authentication and Association (Q10–Q14)

### Q10. Authentication Algorithm

Authentication frames (#5 and #6) use **Open System** algorithm (`Authentication Algorithm: 0`).

### Q11. Auth Request Addresses and Auth Response Status

Authentication request (frame #5):
- Source: **00:12:f0:1c:3e:82**
- Destination: **00:16:b6:f7:1d:51**

Authentication response (frame #6):
- Status code: **0x0000 (Successful)**

### Q12. Association Request Contents

Association Request is frame **#7**. Station provides:
- Capabilities: **0x3104**
- Listen Interval: **0x000a** (10)
- SSID: **30 Munroe St**

### Q13. Association Response Status and AID

Association Response is frame **#8**:
- Status code: **0x0000 (Successful)**
- Association ID (AID): **0x0001**

### Q14. Management Frame Sequence (Probe -> Association)

Observed sequence:
1. **#3** Probe Request
2. **#4** Probe Response
3. **#5** Authentication Request
4. **#6** Authentication Response
5. **#7** Association Request
6. **#8** Association Response

---

## Part 4: Data Frames and Structure (Q15–Q18)

### Q15. Data Frame Address Fields and Roles

Data frame is frame **#9** (`Type/Subtype 0x0020`) with `To DS=1`, `From DS=0`.

Address roles in this frame:
- Receiver (RA / Address 1): **00:16:b6:f7:1d:51** (AP)
- Transmitter (TA / Address 2): **00:12:f0:1c:3e:82** (station)
- Address 3 (Destination field): **00:16:b6:f7:1d:51** in this synthetic example

So 3 MAC address fields are present (plus BSSID context in dissector output).

### Q16. Frame Control Type/Subtype Values

From observed frames:
- Data frame (#9): **0x0020** (Type 2, Subtype 0)
- Beacon frame (#1): **0x0008** (Type 0, Subtype 8)
- ACK frame (#10): **0x001d** (Type 1, Subtype 13)

### Q17. Duration/ID Field in Data Frame

Frame #9 has **Duration = 0 microseconds**.

### Q18. ACK Frame Structure and Relationship to Previous Data Frame

ACK frame is **#10**:
- Type/Subtype: `0x001d`
- Contains one address field: Receiver address **00:12:f0:1c:3e:82**

This matches the transmitter/source station of preceding data frame #9, so #10 acknowledges #9.
