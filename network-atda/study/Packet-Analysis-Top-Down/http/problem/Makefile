# HTTP Lab — Makefile
# Usage:
#   make open-basic          Open the basic HTTP trace in Wireshark
#   make open-conditional    Open the conditional GET trace
#   make open-long           Open the long document trace
#   make open-embedded       Open the embedded objects trace
#   make filter-basic        CLI analysis of basic trace with tshark
#   make verify              Verify answer completeness
#   make test                Alias of verify for automated checks
#   make summary             Print packet summary of all traces
#   make clean               Remove temporary files

WIRESHARK := wireshark
TSHARK    := tshark
DATA_DIR  := data

BASIC_TRACE       := $(DATA_DIR)/http-basic.pcapng
CONDITIONAL_TRACE := $(DATA_DIR)/http-conditional.pcapng
LONG_TRACE        := $(DATA_DIR)/http-long-document.pcapng
EMBEDDED_TRACE    := $(DATA_DIR)/http-embedded-objects.pcapng

.PHONY: open-basic open-conditional open-long open-embedded filter-basic filter-conditional filter-long filter-embedded summary verify test clean help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

open-basic: ## Open the basic HTTP trace in Wireshark GUI
	$(WIRESHARK) $(BASIC_TRACE) &

open-conditional: ## Open the conditional GET trace in Wireshark GUI
	$(WIRESHARK) $(CONDITIONAL_TRACE) &

open-long: ## Open the long document trace in Wireshark GUI
	$(WIRESHARK) $(LONG_TRACE) &

open-embedded: ## Open the embedded objects trace in Wireshark GUI
	$(WIRESHARK) $(EMBEDDED_TRACE) &

filter-basic: ## Display HTTP packets from basic trace via tshark
	$(TSHARK) -r $(BASIC_TRACE) -Y "http" -T fields \
		-e frame.number -e ip.src -e ip.dst \
		-e http.request.method -e http.request.uri \
		-e http.response.code -e http.content_length

filter-conditional: ## Display HTTP packets from conditional trace via tshark
	$(TSHARK) -r $(CONDITIONAL_TRACE) -Y "http" -T fields \
		-e frame.number -e http.request.method \
		-e http.response.code -e http.response.phrase \
		-e http.last_modified -e http.request.line

filter-long: ## Display TCP segment count for long document trace
	@echo "=== HTTP packets ==="
	$(TSHARK) -r $(LONG_TRACE) -Y "http" | head -20
	@echo ""
	@echo "=== Total TCP data segments from server ==="
	$(TSHARK) -r $(LONG_TRACE) -Y "tcp.len > 0 && ip.src == 128.119.245.12" | wc -l

filter-embedded: ## Display all HTTP GET requests in embedded objects trace
	$(TSHARK) -r $(EMBEDDED_TRACE) -Y "http.request.method == GET" -T fields \
		-e frame.number -e ip.dst -e http.request.uri -e http.referer

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
