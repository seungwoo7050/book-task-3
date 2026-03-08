# Packet Analysis — Aggregate Verification

LABS := http dns tcp-udp ip-icmp ethernet-arp wireless-802.11 tls-ssl
REQUIRED_TRACES := \
	http/problem/data/http-basic.pcapng \
	http/problem/data/http-conditional.pcapng \
	http/problem/data/http-long-document.pcapng \
	http/problem/data/http-embedded-objects.pcapng \
	dns/problem/data/dns-nslookup.pcapng \
	dns/problem/data/dns-web-browsing.pcapng \
	tcp-udp/problem/data/tcp-upload.pcapng \
	tcp-udp/problem/data/udp-dns.pcapng \
	ip-icmp/problem/data/ip-traceroute.pcapng \
	ip-icmp/problem/data/ip-fragmentation.pcapng \
	ethernet-arp/problem/data/ethernet-arp.pcapng \
	wireless-802.11/problem/data/wireless-trace.pcap \
	tls-ssl/problem/data/tls-trace.pcap

.PHONY: help verify test check-traces

help: ## Show available targets
	@echo "Available targets:"
	@echo "  verify        - Run answer verification for all packet-analysis labs"
	@echo "  test          - Alias of verify"
	@echo "  check-traces  - Ensure required trace files exist"

verify: ## Run verification for all labs
	@set -e; \
	for lab in $(LABS); do \
		echo "===== $$lab ====="; \
		$(MAKE) -C "$$lab/problem" test; \
		echo ""; \
	done

test: verify ## Alias used by repository-wide validation

check-traces: ## Verify required trace files exist
	@set -e; \
	missing=0; \
	for trace in $(REQUIRED_TRACES); do \
		if [ ! -f "$$trace" ]; then \
			echo "MISSING: $$trace"; \
			missing=1; \
		fi; \
	done; \
	if [ "$$missing" -eq 0 ]; then \
		echo "PASS: all required trace files exist"; \
	else \
		echo "FAIL: one or more required trace files are missing"; \
		exit 1; \
	fi
