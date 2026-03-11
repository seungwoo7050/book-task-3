# Makefile for TLS/SSL Wireshark Lab
# Usage: make help

TRACE = data/tls-trace.pcap
WIRESHARK := wireshark
TSHARK := tshark

.PHONY: help open handshake client-hello server-hello certs app-data cipher-change records verify test clean

help:
	@echo "Available targets:"
	@echo "  open           - Open trace file in Wireshark"
	@echo "  handshake      - Filter all TLS handshake messages"
	@echo "  client-hello   - Filter ClientHello messages"
	@echo "  server-hello   - Filter ServerHello messages"
	@echo "  certs          - Filter Certificate messages"
	@echo "  cipher-change  - Filter ChangeCipherSpec messages"
	@echo "  app-data       - Filter Application Data records"
	@echo "  records        - Show TLS record type summary"
	@echo "  verify         - Verify answer completeness"
	@echo "  test           - Alias of verify for automated checks"
	@echo "  clean          - Remove temporary files"
	@echo ""
	@echo "Trace file: $(TRACE)"

open:
	$(WIRESHARK) $(TRACE) &

handshake:
	$(TSHARK) -r $(TRACE) -Y "tls.handshake" \
		-T fields -e frame.number -e ip.src -e ip.dst -e tls.handshake.type

client-hello:
	$(TSHARK) -r $(TRACE) -Y "tls.handshake.type == 1" \
		-T fields -e frame.number -e tls.handshake.version -e tls.handshake.ciphersuite \
		-e tls.handshake.extensions_server_name

server-hello:
	$(TSHARK) -r $(TRACE) -Y "tls.handshake.type == 2" \
		-T fields -e frame.number -e tls.handshake.version -e tls.handshake.ciphersuite

certs:
	$(TSHARK) -r $(TRACE) -Y "tls.handshake.type == 11" \
		-T fields -e frame.number -e tls.handshake.certificate_length \
		-e x509sat.utf8String -e x509ce.dNSName

cipher-change:
	$(TSHARK) -r $(TRACE) -Y "tls.change_cipher_spec" \
		-T fields -e frame.number -e ip.src -e ip.dst

app-data:
	$(TSHARK) -r $(TRACE) -Y "tls.record.content_type == 23" \
		-T fields -e frame.number -e ip.src -e ip.dst -e tls.record.length | head -30

records:
	$(TSHARK) -r $(TRACE) -Y "tls" \
		-T fields -e tls.record.content_type | sort | uniq -c | sort -rn

verify:
	bash script/verify_answers.sh

test: verify

clean:
	find . -name '*.tmp' -delete 2>/dev/null || true
	find . -name '.DS_Store' -delete 2>/dev/null || true
