.PHONY: all verify test app-install app-build app-test run-ios run-android benchmark clean

APP_DIR := ../react-native

all: test

verify:
	bash script/verify_task.sh

test: verify

app-install:
	cd $(APP_DIR) && test -d node_modules || npm install --no-audit --no-fund

app-build: app-install
	cd $(APP_DIR) && npm run typecheck

app-test: app-install
	cd $(APP_DIR) && npm test

run-ios: app-install
	cd $(APP_DIR) && npm run ios

run-android: app-install
	cd $(APP_DIR) && npm run android

benchmark: app-install
	cd $(APP_DIR) && npm run benchmark

clean:
	rm -rf $(APP_DIR)/node_modules $(APP_DIR)/ios/build $(APP_DIR)/android/build $(APP_DIR)/benchmarks
