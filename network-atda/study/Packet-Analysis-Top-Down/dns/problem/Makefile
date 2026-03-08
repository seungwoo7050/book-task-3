# DNS Lab — Makefile
# Usage:
#   make open-nslookup       Open the nslookup DNS trace in Wireshark
#   make open-browsing       Open the web browsing DNS trace in Wireshark
#   make filter-queries      Show all DNS queries via tshark
#   make filter-responses    Show all DNS responses via tshark
#   make verify              Verify answer completeness
#   make test                Alias of verify for automated checks
#   make summary             Print packet count summary
#   make clean               Remove temporary files

WIRESHARK := wireshark
TSHARK    := tshark
DATA_DIR  := data

NSLOOKUP_TRACE := $(DATA_DIR)/dns-nslookup.pcapng
BROWSING_TRACE := $(DATA_DIR)/dns-web-browsing.pcapng

.PHONY: open-nslookup open-browsing filter-queries filter-responses filter-browsing summary verify test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

open-nslookup: ## Open the nslookup trace in Wireshark GUI
	$(WIRESHARK) $(NSLOOKUP_TRACE) &

open-browsing: ## Open the web browsing DNS trace in Wireshark GUI
	$(WIRESHARK) $(BROWSING_TRACE) &

filter-queries: ## Display all DNS query packets via tshark
	$(TSHARK) -r $(NSLOOKUP_TRACE) -Y "dns.flags.response == 0" -T fields \
		-e frame.number -e ip.dst -e dns.qry.name -e dns.qry.type

filter-responses: ## Display all DNS response packets via tshark
	$(TSHARK) -r $(NSLOOKUP_TRACE) -Y "dns.flags.response == 1" -T fields \
		-e frame.number -e dns.qry.name -e dns.resp.type \
		-e dns.a -e dns.aaaa -e dns.cname -e dns.resp.ttl

filter-browsing: ## Display DNS queries triggered by web browsing
	$(TSHARK) -r $(BROWSING_TRACE) -Y "dns" -T fields \
		-e frame.number -e dns.flags.response \
		-e dns.qry.name -e dns.qry.type -e dns.a

summary: ## Print packet count summary for all traces
	@for f in $(DATA_DIR)/*.pcapng; do \
		echo "=== $$f ==="; \
		$(TSHARK) -r "$$f" -Y "dns" 2>/dev/null | wc -l; \
		echo ""; \
	done

verify: ## Verify completeness of solve answers
	bash script/verify_answers.sh

test: verify ## Alias used by repository-wide validation

clean: ## Remove temporary files
	find . -name '*.tmp' -delete 2>/dev/null || true
	find . -name '.DS_Store' -delete 2>/dev/null || true
