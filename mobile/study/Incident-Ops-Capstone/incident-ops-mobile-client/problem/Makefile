.PHONY: all verify test app-install app-build app-test server-install server-test demo-e2e clean

APP_DIR := ../react-native
SERVER_DIR := ../node-server

all: test

verify:
	bash script/verify_task.sh

test: verify

app-install:
	cd $(APP_DIR) && npm install --no-audit --no-fund

app-build: app-install
	cd $(APP_DIR) && npm run typecheck

app-test: app-install
	cd $(APP_DIR) && npm test

server-install:
	cd $(SERVER_DIR) && npm install --no-audit --no-fund

server-test: server-install
	cd $(SERVER_DIR) && npm test

demo-e2e: server-install
	cd $(SERVER_DIR) && npm run demo-e2e
	@if command -v maestro >/dev/null 2>&1; then \
		cd $(APP_DIR) && maestro test maestro/smoke-login-create.yaml; \
	else \
		echo "maestro not installed; skipped device flow"; \
	fi

clean:
	rm -f ../demo/*.log ../demo/*.json
