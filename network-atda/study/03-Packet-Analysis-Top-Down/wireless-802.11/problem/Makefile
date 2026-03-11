# Makefile for 802.11 Wireless Wireshark Lab
# Usage: make help

TRACE = data/wireless-trace.pcap
WIRESHARK := wireshark
TSHARK := tshark

.PHONY: help open beacons probes auth assoc data ack frames-summary verify test clean

help:
	@echo "Available targets:"
	@echo "  open            - Open trace file in Wireshark"
	@echo "  beacons         - Filter beacon frames"
	@echo "  probes          - Filter probe request/response frames"
	@echo "  auth            - Filter authentication frames"
	@echo "  assoc           - Filter association request/response frames"
	@echo "  data            - Filter 802.11 data frames"
	@echo "  ack             - Filter ACK control frames"
	@echo "  frames-summary  - Show frame type/subtype summary"
	@echo "  verify          - Verify answer completeness"
	@echo "  test            - Alias of verify for automated checks"
	@echo "  clean           - Remove temporary files"
	@echo ""
	@echo "Trace file: $(TRACE)"

open:
	$(WIRESHARK) $(TRACE) &

beacons:
	$(TSHARK) -r $(TRACE) -Y "wlan.fc.type_subtype == 0x08" \
		-T fields -e frame.number -e wlan.sa -e wlan.ssid -e wlan.fixed.beacon

probes:
	$(TSHARK) -r $(TRACE) -Y "wlan.fc.type_subtype == 0x04 || wlan.fc.type_subtype == 0x05" \
		-T fields -e frame.number -e wlan.fc.type_subtype -e wlan.sa -e wlan.da -e wlan.ssid

auth:
	$(TSHARK) -r $(TRACE) -Y "wlan.fc.type_subtype == 0x0b" \
		-T fields -e frame.number -e wlan.sa -e wlan.da -e wlan.fixed.auth.alg -e wlan.fixed.status_code

assoc:
	$(TSHARK) -r $(TRACE) -Y "wlan.fc.type_subtype == 0x00 || wlan.fc.type_subtype == 0x01" \
		-T fields -e frame.number -e wlan.fc.type_subtype -e wlan.sa -e wlan.da -e wlan.fixed.status_code -e wlan.fixed.aid

data:
	$(TSHARK) -r $(TRACE) -Y "wlan.fc.type == 2" \
		-T fields -e frame.number -e wlan.sa -e wlan.da -e wlan.bssid -e wlan.fc.tods -e wlan.fc.fromds

ack:
	$(TSHARK) -r $(TRACE) -Y "wlan.fc.type_subtype == 0x1d" \
		-T fields -e frame.number -e wlan.ra -e wlan.duration

frames-summary:
	$(TSHARK) -r $(TRACE) -T fields -e wlan.fc.type -e wlan.fc.type_subtype | sort | uniq -c | sort -rn

verify:
	bash script/verify_answers.sh

test: verify

clean:
	find . -name '*.tmp' -delete 2>/dev/null || true
	find . -name '.DS_Store' -delete 2>/dev/null || true
