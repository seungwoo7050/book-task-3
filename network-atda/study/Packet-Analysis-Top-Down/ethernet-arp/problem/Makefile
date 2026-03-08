# Ethernet & ARP Lab — Makefile
# Usage:
#   make open-trace          Open the ARP trace in Wireshark
#   make filter-arp          Show ARP packets via tshark
#   make filter-ethernet     Show Ethernet header info via tshark
#   make verify              Verify answer completeness
#   make test                Alias of verify for automated checks
#   make summary             Print packet count summary
#   make clean               Remove temporary files

WIRESHARK := wireshark
TSHARK    := tshark
DATA_DIR  := data

ARP_TRACE := $(DATA_DIR)/ethernet-arp.pcapng

.PHONY: open-trace filter-arp filter-ethernet filter-broadcast summary verify test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

open-trace: ## Open the ARP trace in Wireshark GUI
	$(WIRESHARK) $(ARP_TRACE) &

filter-arp: ## Display all ARP packets via tshark
	$(TSHARK) -r $(ARP_TRACE) -Y "arp" -T fields \
		-e frame.number -e eth.src -e eth.dst \
		-e arp.opcode -e arp.src.hw_mac -e arp.src.proto_ipv4 \
		-e arp.dst.hw_mac -e arp.dst.proto_ipv4

filter-ethernet: ## Display Ethernet header info for first 20 packets
	$(TSHARK) -r $(ARP_TRACE) -T fields \
		-e frame.number -e eth.src -e eth.dst -e eth.type \
		| head -20

filter-broadcast: ## Show broadcast frames
	$(TSHARK) -r $(ARP_TRACE) -Y "eth.dst == ff:ff:ff:ff:ff:ff" -T fields \
		-e frame.number -e eth.src -e eth.type

summary: ## Print packet count summary
	@echo "=== $(ARP_TRACE) ==="
	$(TSHARK) -r $(ARP_TRACE) -q -z io,stat,0 2>/dev/null | head -10

verify: ## Verify completeness of solve answers
	bash script/verify_answers.sh

test: verify ## Alias used by repository-wide validation

clean: ## Remove temporary files
	find . -name '*.tmp' -delete 2>/dev/null || true
	find . -name '.DS_Store' -delete 2>/dev/null || true
