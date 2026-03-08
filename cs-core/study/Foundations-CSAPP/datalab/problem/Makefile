# Data Lab Makefile
# Builds the btest test harness and provides convenience targets.

CC       = gcc
UNAME_S  := $(shell uname -s)
UNAME_M  := $(shell uname -m)
ARCH_FLAGS := -m32
REPO_ROOT := $(abspath ../../../..)
RESTORE_SCRIPT := $(REPO_ROOT)/study/tools/restore_csapp_self_study_assets.py
DOCKERFILE := $(REPO_ROOT)/study/tools/Dockerfile.csapp-official
DOCKER_IMAGE := csapp-official-linux-amd64
DOCKER_RUN = docker run --rm --platform linux/amd64 -v "$(REPO_ROOT):$(REPO_ROOT)" -w "$(CURDIR)" $(DOCKER_IMAGE) bash -lc
OFFICIAL_DIR := official/datalab-handout

ifeq ($(UNAME_S),Darwin)
ifeq ($(UNAME_M),arm64)
ARCH_FLAGS :=
endif
endif

CFLAGS   = -O1 -Wall -Werror $(ARCH_FLAGS)
LDFLAGS  = $(ARCH_FLAGS) -lm

SRC_DIR  = code
BITS_SRC ?= $(SRC_DIR)/bits.c
BTEST    = btest
DLC      = $(SRC_DIR)/dlc

OBJS     = $(SRC_DIR)/btest.o $(SRC_DIR)/bits.o $(SRC_DIR)/decl.o $(SRC_DIR)/tests.o

# ──────────────────────────────────────────────
# Targets
# ──────────────────────────────────────────────

.PHONY: all clean check test grade restore-official docker-image verify-official help

all: $(BTEST)    ## Build the btest harness

$(BTEST): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

$(SRC_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(SRC_DIR)/bits.o: $(BITS_SRC)
	$(CC) $(CFLAGS) -c -o $@ $<

clean:           ## Remove build artifacts
	rm -f $(BTEST) $(SRC_DIR)/*.o

check:           ## Run dlc to verify operator legality
	$(DLC) $(BITS_SRC)

test: clean $(BTEST)   ## Run btest to check correctness
	./$(BTEST)

grade: $(BTEST)  ## Run the full grading script (dlc + btest)
	bash script/grade.sh

restore-official: ## Restore the official self-study handout locally under official/
	python3 "$(RESTORE_SCRIPT)" datalab

docker-image: ## Build the shared Linux/amd64 verifier image
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE) -f "$(DOCKERFILE)" "$(REPO_ROOT)"

verify-official: restore-official docker-image ## Run official dlc + btest in Linux/amd64 Docker
	cp "$(abspath ../c/src/bits.c)" "$(OFFICIAL_DIR)/bits.c"
	@$(DOCKER_RUN) 'cd "$(CURDIR)/$(OFFICIAL_DIR)" && make clean && make && ./dlc bits.c && ./btest -T 20'

help:            ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
