# Makefile for HTTP/2 and QUIC comparison lab

.PHONY: help http2-overview quic-overview compare verify test clean

help:
	@echo "Available targets:"
	@echo "  http2-overview - Show the condensed HTTP/2 trace"
	@echo "  quic-overview  - Show the condensed QUIC trace"
	@echo "  compare        - Print both traces in sequence"
	@echo "  verify         - Verify answer completeness"
	@echo "  test           - Alias of verify"

http2-overview:
	cat data/http2-trace.tsv

quic-overview:
	cat data/quic-trace.tsv

compare:
	@echo "=== HTTP/2 ==="
	@cat data/http2-trace.tsv
	@echo ""
	@echo "=== QUIC ==="
	@cat data/quic-trace.tsv

verify:
	bash script/verify_answers.sh

test: verify

clean:
	find . -name '.DS_Store' -delete 2>/dev/null || true
