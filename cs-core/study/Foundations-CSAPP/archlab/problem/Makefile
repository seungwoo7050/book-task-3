REPO_ROOT := $(abspath ../../../..)
RESTORE_SCRIPT := $(REPO_ROOT)/study/tools/restore_csapp_self_study_assets.py
DOCKERFILE := $(REPO_ROOT)/study/tools/Dockerfile.csapp-official
DOCKER_IMAGE := csapp-official-linux-amd64
DOCKER_RUN = docker run --rm --platform linux/amd64 -v "$(REPO_ROOT):$(REPO_ROOT)" -w "$(CURDIR)" $(DOCKER_IMAGE) bash -lc
OFFICIAL_DIR := official/archlab-handout
SIM_DIR := $(OFFICIAL_DIR)/sim
Y86_DIR := ../y86
PATCH_SCRIPT := $(abspath $(Y86_DIR)/script/apply_hcl_patches.py)

.PHONY: all status restore-official docker-image sync-official verify-part-a verify-part-b verify-part-c verify-official clean

all: status

status:
	@if [ -d "$(SIM_DIR)" ]; then \
		echo "official simulator restored: $(SIM_DIR)"; \
	else \
		echo "official simulator missing: $(SIM_DIR)"; \
		echo "run 'make restore-official' to restore the public self-study handout."; \
	fi
	@echo "study-owned official hand-in files live under $(Y86_DIR)/"

restore-official:
	python3 "$(RESTORE_SCRIPT)" archlab

docker-image:
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE) -f "$(DOCKERFILE)" "$(REPO_ROOT)"

sync-official: restore-official
	cp "$(abspath $(Y86_DIR)/src/sum.ys)" "$(SIM_DIR)/misc/sum.ys"
	cp "$(abspath $(Y86_DIR)/src/rsum.ys)" "$(SIM_DIR)/misc/rsum.ys"
	cp "$(abspath $(Y86_DIR)/src/copy.ys)" "$(SIM_DIR)/misc/copy.ys"
	cp "$(abspath $(Y86_DIR)/src/ncopy.ys)" "$(SIM_DIR)/pipe/ncopy.ys"
	python3 "$(PATCH_SCRIPT)" "$(SIM_DIR)/seq/seq-full.hcl" "$(SIM_DIR)/pipe/pipe-full.hcl"

verify-part-a: sync-official docker-image
	@$(DOCKER_RUN) 'cd "$(CURDIR)/$(SIM_DIR)/misc" && make clean >/dev/null && make CFLAGS="-Wall -O1 -g -fcommon" LCFLAGS="-O1 -fcommon" >/dev/null && ./yas sum.ys >/dev/null && ./yis sum.yo > /tmp/sum.out && grep -Eq "%rax:.*0x0000000000000cba" /tmp/sum.out && ./yas rsum.ys >/dev/null && ./yis rsum.yo > /tmp/rsum.out && grep -Eq "%rax:.*0x0000000000000cba" /tmp/rsum.out && ./yas copy.ys >/dev/null && ./yis copy.yo > /tmp/copy.out && grep -Eq "%rax:.*0x0000000000000cba" /tmp/copy.out'

verify-part-b: sync-official docker-image
	@$(DOCKER_RUN) 'cd "$(CURDIR)/$(SIM_DIR)/misc" && make clean >/dev/null && make CFLAGS="-Wall -O1 -g -fcommon" LCFLAGS="-O1 -fcommon" >/dev/null && cd ../seq && make clean >/dev/null && make ssim VERSION=full GUIMODE= TKLIBS= TKINC= CFLAGS="-Wall -O2 -fcommon" >/dev/null && cd ../ptest && make SIM=../seq/ssim TFLAGS=-i'

verify-part-c: sync-official docker-image
	@$(DOCKER_RUN) 'cd "$(CURDIR)/$(SIM_DIR)/misc" && make clean >/dev/null && make CFLAGS="-Wall -O1 -g -fcommon" LCFLAGS="-O1 -fcommon" >/dev/null && cd ../pipe && make clean >/dev/null && make psim VERSION=full GUIMODE= TKLIBS= TKINC= CFLAGS="-Wall -O2 -fcommon" >/dev/null && make drivers >/dev/null && cd ../ptest && make SIM=../pipe/psim TFLAGS=-i && cd ../pipe && ./correctness.pl -f ncopy.ys && ./benchmark.pl -f ncopy.ys'

verify-official: verify-part-a verify-part-b verify-part-c

clean:
	@true
