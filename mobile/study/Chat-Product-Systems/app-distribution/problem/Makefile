.PHONY: all verify test app-build app-test release-rehearsal clean

all: test

verify:
	bash script/verify_task.sh

test: verify

app-build:
	cd ../react-native && test -d node_modules || npm install --no-audit --no-fund
	cd ../react-native && npm run typecheck

app-test:
	cd ../react-native && test -d node_modules || npm install --no-audit --no-fund
	cd ../react-native && npm test

release-rehearsal:
	cd ../react-native && test -d node_modules || npm install --no-audit --no-fund
	cd ../react-native && npm run release:rehearsal

clean:
	rm -rf ../react-native/release
