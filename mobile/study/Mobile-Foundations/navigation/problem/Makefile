.PHONY: all verify test app-install app-build app-test run-ios run-android test-deeplink-ios test-deeplink-android clean

APP_DIR := ../react-native

all: test

verify:
	bash script/verify_task.sh

test: verify

app-install:
	cd $(APP_DIR) && npm install

app-build:
	cd $(APP_DIR) && npm run typecheck

app-test:
	cd $(APP_DIR) && npm test

run-ios:
	cd $(APP_DIR) && npm run ios

run-android:
	cd $(APP_DIR) && npm run android

test-deeplink-ios:
	@if command -v xcrun >/dev/null 2>&1; then xcrun simctl openurl booted "myapp://detail/123"; else echo "xcrun not found"; fi

test-deeplink-android:
	@if command -v adb >/dev/null 2>&1; then adb shell am start -W -a android.intent.action.VIEW -d "myapp://detail/123"; else echo "adb not found"; fi

clean:
	rm -rf $(APP_DIR)/node_modules $(APP_DIR)/ios/build $(APP_DIR)/android/build
