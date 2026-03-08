.PHONY: all verify test app-build app-test server-test demo-e2e clean

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

server-test:
	cd ../node-server && test -d node_modules || npm install --no-audit --no-fund
	cd ../node-server && npm test

demo-e2e:
	mkdir -p ../demo
	cd ../node-server && test -d node_modules || npm install --no-audit --no-fund
	cd ../node-server && npm run demo-e2e

clean:
	rm -f ../demo/*.log ../demo/*.json
