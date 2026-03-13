# Packet Analysis 전체 검증용 Makefile

LABS := http dns tcp-udp ip-icmp ethernet-arp wireless-802.11 tls-ssl http2-quic
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
	tls-ssl/problem/data/tls-trace.pcap \
	http2-quic/problem/data/http2-trace.tsv \
	http2-quic/problem/data/quic-trace.tsv

.PHONY: help verify test check-traces

help: ## 사용 가능한 target을 보여 준다
	@echo "Available targets:"
	@echo "  verify        - Run answer verification for all packet-analysis labs"
	@echo "  test          - Alias of verify"
	@echo "  check-traces  - Ensure required trace files exist"

verify: ## 모든 packet-analysis lab에 대해 검증을 실행한다
	@set -e; \
	for lab in $(LABS); do \
		echo "===== $$lab ====="; \
		$(MAKE) -C "$$lab/problem" test; \
		echo ""; \
	done

test: verify ## 저장소 수준 검증에서 사용하는 alias

check-traces: ## 필요한 trace file이 모두 있는지 확인한다
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
