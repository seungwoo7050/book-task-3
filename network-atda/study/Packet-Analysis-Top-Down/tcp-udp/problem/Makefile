# TCP & UDP Lab — Makefile
# Usage:
#   make open-tcp            Open the TCP upload trace in Wireshark
#   make open-udp            Open the UDP DNS trace in Wireshark
#   make filter-handshake    Show TCP 3-way handshake packets
#   make filter-data         Show TCP data segments
#   make filter-udp          Show UDP packets
#   make verify              Verify answer completeness
#   make test                Alias of verify for automated checks
#   make summary             Print packet count summary
#   make clean               Remove temporary files

WIRESHARK := wireshark
TSHARK    := tshark
DATA_DIR  := data

TCP_TRACE := $(DATA_DIR)/tcp-upload.pcapng
UDP_TRACE := $(DATA_DIR)/udp-dns.pcapng

.PHONY: open-tcp open-udp filter-handshake filter-data filter-retransmissions filter-udp summary verify test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

open-tcp: ## Open the TCP upload trace in Wireshark GUI
	$(WIRESHARK) $(TCP_TRACE) &

open-udp: ## Open the UDP DNS trace in Wireshark GUI
	$(WIRESHARK) $(UDP_TRACE) &

filter-handshake: ## Show the TCP 3-way handshake (SYN, SYN-ACK, ACK)
	$(TSHARK) -r $(TCP_TRACE) -Y "tcp.flags.syn == 1 || (tcp.flags.ack == 1 && tcp.seq == 1 && tcp.ack == 1)" \
		-T fields -e frame.number -e ip.src -e ip.dst \
		-e tcp.srcport -e tcp.dstport -e tcp.flags -e tcp.seq -e tcp.ack

filter-data: ## Show TCP data segments (payload > 0)
	$(TSHARK) -r $(TCP_TRACE) -Y "tcp.len > 0" -T fields \
		-e frame.number -e tcp.seq -e tcp.ack -e tcp.len -e tcp.window_size \
		| head -30

filter-retransmissions: ## Show TCP retransmissions
	$(TSHARK) -r $(TCP_TRACE) -Y "tcp.analysis.retransmission" -T fields \
		-e frame.number -e tcp.seq -e tcp.len -e frame.time_relative

filter-udp: ## Show all UDP packets from DNS trace
	$(TSHARK) -r $(UDP_TRACE) -Y "udp" -T fields \
		-e frame.number -e ip.src -e ip.dst \
		-e udp.srcport -e udp.dstport -e udp.length

summary: ## Print packet count summary for all traces
	@for f in $(DATA_DIR)/*.pcapng; do \
		echo "=== $$f ==="; \
		$(TSHARK) -r "$$f" -q -z io,stat,0 2>/dev/null | head -10; \
		echo ""; \
	done

verify: ## Verify completeness of solve answers
	bash script/verify_answers.sh

test: verify ## Alias used by repository-wide validation

clean: ## Remove temporary files
	find . -name '*.tmp' -delete 2>/dev/null || true
	find . -name '.DS_Store' -delete 2>/dev/null || true
