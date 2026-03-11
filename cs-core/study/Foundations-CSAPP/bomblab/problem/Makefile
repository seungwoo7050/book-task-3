# Bomb Lab problem Makefile

REPO_ROOT := $(abspath ../../../..)
RESTORE_SCRIPT := $(REPO_ROOT)/study/scripts/restore_csapp_self_study_assets.py
DOCKERFILE := $(REPO_ROOT)/study/scripts/Dockerfile.csapp-official
DOCKER_IMAGE := csapp-official-linux-amd64
DOCKER_RUN = docker run --rm --platform linux/amd64 -v "$(REPO_ROOT):$(REPO_ROOT)" -w "$(CURDIR)" $(DOCKER_IMAGE) bash -lc
OFFICIAL_DIR := official/bomb
BOMB = $(OFFICIAL_DIR)/bomb
SOLUTION = data/solutions.txt

.PHONY: all status restore-official docker-image disas strings symbols run test verify-official help clean

all: status

status:
	@if [ -f "$(BOMB)" ]; then \
		echo "bomb present: $(BOMB)"; \
	else \
		echo "bomb missing: $(BOMB)"; \
		echo "run 'make restore-official' to restore the public self-study bomb."; \
	fi

disas:
	@if [ -f "$(BOMB)" ]; then \
		objdump -d "$(BOMB)" > bomb_disas.txt; \
		echo "wrote bomb_disas.txt"; \
	else \
		echo "Error: $(BOMB) not found."; \
		exit 1; \
	fi

strings:
	@if [ -f "$(BOMB)" ]; then \
		strings "$(BOMB)" > bomb_strings.txt; \
		echo "wrote bomb_strings.txt"; \
	else \
		echo "Error: $(BOMB) not found."; \
		exit 1; \
	fi

symbols:
	@if [ -f "$(BOMB)" ]; then \
		nm "$(BOMB)" | sort > bomb_symbols.txt; \
		echo "wrote bomb_symbols.txt"; \
	else \
		echo "Error: $(BOMB) not found."; \
		exit 1; \
	fi

run:
	@$(DOCKER_RUN) '"$(BOMB)"'

test:
	@if [ ! -f "$(BOMB)" ] || [ ! -f "$(SOLUTION)" ]; then \
		echo "Error: restored bomb or solution file not found."; \
		exit 1; \
	fi
	@$(DOCKER_RUN) '"$(BOMB)" "$(SOLUTION)"'

restore-official:
	python3 "$(RESTORE_SCRIPT)" bomblab

docker-image:
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE) -f "$(DOCKERFILE)" "$(REPO_ROOT)"

verify-official: restore-official docker-image test

clean:
	rm -f bomb_disas.txt bomb_strings.txt bomb_symbols.txt

help:
	@grep -E '^[a-zA-Z_-]+:.*$$' $(MAKEFILE_LIST)
