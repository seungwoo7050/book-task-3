# Attack Lab problem Makefile

REPO_ROOT := $(abspath ../../../..)
RESTORE_SCRIPT := $(REPO_ROOT)/study/tools/restore_csapp_self_study_assets.py
DOCKERFILE := $(REPO_ROOT)/study/tools/Dockerfile.csapp-official
DOCKER_IMAGE := csapp-official-linux-amd64
DOCKER_RUN = docker run --rm --platform linux/amd64 -v "$(REPO_ROOT):$(REPO_ROOT)" -w "$(CURDIR)" $(DOCKER_IMAGE) bash -lc
OFFICIAL_DIR := official/target1
CTARGET = $(OFFICIAL_DIR)/ctarget
RTARGET = $(OFFICIAL_DIR)/rtarget
HEX2RAW = $(OFFICIAL_DIR)/hex2raw
COOKIE = $(OFFICIAL_DIR)/cookie.txt
DATA_DIR = data

.PHONY: all status restore-official docker-image disas-ct disas-rt farm phase1 phase2 phase3 phase4 phase5 verify-official clean

all: status

status:
	@if [ -f "$(CTARGET)" ]; then echo "ctarget present: $(CTARGET)"; else echo "ctarget missing: $(CTARGET)"; fi
	@if [ -f "$(RTARGET)" ]; then echo "rtarget present: $(RTARGET)"; else echo "rtarget missing: $(RTARGET)"; fi
	@if [ -f "$(HEX2RAW)" ]; then echo "hex2raw present: $(HEX2RAW)"; else echo "hex2raw missing: $(HEX2RAW)"; fi
	@if [ -f "$(COOKIE)" ]; then echo "cookie present: $(COOKIE)"; else echo "cookie missing: $(COOKIE)"; fi

restore-official:
	python3 "$(RESTORE_SCRIPT)" attacklab

docker-image:
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE) -f "$(DOCKERFILE)" "$(REPO_ROOT)"

disas-ct:
	@if [ -f "$(CTARGET)" ]; then objdump -d "$(CTARGET)" > ctarget_disas.txt; else echo "Error: $(CTARGET) not found."; exit 1; fi

disas-rt:
	@if [ -f "$(RTARGET)" ]; then objdump -d "$(RTARGET)" > rtarget_disas.txt; else echo "Error: $(RTARGET) not found."; exit 1; fi

farm:
	@if [ -f rtarget_disas.txt ]; then sed -n '/start_farm/,/end_farm/p' rtarget_disas.txt > farm_gadgets.txt; else echo "Run 'make disas-rt' first."; exit 1; fi

phase1:
	@$(DOCKER_RUN) '"$(HEX2RAW)" < "$(DATA_DIR)/phase1.txt" | "$(CTARGET)" -q'

phase2:
	@$(DOCKER_RUN) '"$(HEX2RAW)" < "$(DATA_DIR)/phase2.txt" | "$(CTARGET)" -q'

phase3:
	@$(DOCKER_RUN) '"$(HEX2RAW)" < "$(DATA_DIR)/phase3.txt" | "$(CTARGET)" -q'

phase4:
	@$(DOCKER_RUN) '"$(HEX2RAW)" < "$(DATA_DIR)/phase4.txt" | "$(RTARGET)" -q'

phase5:
	@$(DOCKER_RUN) '"$(HEX2RAW)" < "$(DATA_DIR)/phase5.txt" | "$(RTARGET)" -q'

verify-official: restore-official docker-image phase1 phase2 phase3 phase4 phase5

clean:
	rm -f ctarget_disas.txt rtarget_disas.txt farm_gadgets.txt
