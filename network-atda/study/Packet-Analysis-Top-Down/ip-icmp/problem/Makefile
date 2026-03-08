# IP & ICMP Lab — Makefile
# Usage:
#   make open-traceroute     Open the traceroute trace in Wireshark
#   make open-fragmentation  Open the fragmentation trace in Wireshark
#   make filter-icmp         Show ICMP packets via tshark
#   make filter-fragments    Show fragmented IP packets
#   make verify              Verify answer completeness
#   make test                Alias of verify for automated checks
#   make summary             Print packet count summary
#   make clean               Remove temporary files

WIRESHARK := wireshark
TSHARK    := tshark
DATA_DIR  := data

TRACEROUTE_TRACE    := $(DATA_DIR)/ip-traceroute.pcapng
FRAGMENTATION_TRACE := $(DATA_DIR)/ip-fragmentation.pcapng

.PHONY: open-traceroute open-fragmentation filter-icmp filter-fragments filter-ttl summary verify test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

open-traceroute: ## Open the traceroute trace in Wireshark GUI
	$(WIRESHARK) $(TRACEROUTE_TRACE) &

open-fragmentation: ## Open the fragmentation trace in Wireshark GUI
	$(WIRESHARK) $(FRAGMENTATION_TRACE) &

filter-icmp: ## Show all ICMP packets from traceroute trace
	$(TSHARK) -r $(TRACEROUTE_TRACE) -Y "icmp" -T fields \
		-e frame.number -e ip.src -e ip.dst \
		-e ip.ttl -e icmp.type -e icmp.code -e ip.id

filter-fragments: ## Show fragmented IP packets
	$(TSHARK) -r $(FRAGMENTATION_TRACE) -Y "ip.flags.mf == 1 || ip.frag_offset > 0" \
		-T fields -e frame.number -e ip.id -e ip.flags.mf \
		-e ip.frag_offset -e ip.len

filter-ttl: ## Show TTL values for ICMP echo requests
	$(TSHARK) -r $(TRACEROUTE_TRACE) -Y "icmp.type == 8" -T fields \
		-e frame.number -e ip.ttl -e ip.id -e ip.dst

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
