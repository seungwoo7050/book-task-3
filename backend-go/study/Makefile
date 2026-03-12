.PHONY: test-all test-new test-migrated test-infra test-runtime test-portfolio-unit test-portfolio-repro check-docs check-notion release-check

MODULE_DIRS := \
	00-go-fundamentals/01-go-syntax-and-tooling/solution/go \
	00-go-fundamentals/02-types-errors-interfaces/solution/go \
	00-go-fundamentals/03-testing-and-debugging/solution/go \
	01-backend-core/04-sql-and-data-modeling/solution/go \
	01-backend-core/05-http-rest-basics/solution/go \
	01-backend-core/06-go-api-standard/solution/go \
	01-backend-core/07-auth-session-jwt/solution/go \
	01-backend-core/08-sql-store-api/solution/go \
	01-backend-core/09-cache-migrations-observability/solution/go \
	01-backend-core/10-concurrency-patterns/solution/go \
	01-backend-core/11-rate-limiter/solution/go \
	02-distributed-systems/12-grpc-microservices/solution/go \
	02-distributed-systems/13-distributed-log-core/solution/go \
	03-platform-engineering/14-cockroach-tx/solution/go \
	03-platform-engineering/15-event-pipeline/solution/go \
	04-capstone/17-game-store-capstone/solution/go \
	05-portfolio-projects/18-workspace-saas-api/solution/go

NEW_MODULE_DIRS := \
	00-go-fundamentals/01-go-syntax-and-tooling/solution/go \
	00-go-fundamentals/02-types-errors-interfaces/solution/go \
	00-go-fundamentals/03-testing-and-debugging/solution/go \
	01-backend-core/04-sql-and-data-modeling/solution/go \
	01-backend-core/05-http-rest-basics/solution/go \
	01-backend-core/07-auth-session-jwt/solution/go \
	01-backend-core/08-sql-store-api/solution/go \
	01-backend-core/09-cache-migrations-observability/solution/go \
	05-portfolio-projects/18-workspace-saas-api/solution/go

MIGRATED_MODULE_DIRS := \
	01-backend-core/06-go-api-standard/solution/go \
	01-backend-core/10-concurrency-patterns/solution/go \
	01-backend-core/11-rate-limiter/solution/go \
	02-distributed-systems/12-grpc-microservices/solution/go \
	02-distributed-systems/13-distributed-log-core/solution/go \
	03-platform-engineering/14-cockroach-tx/solution/go \
	03-platform-engineering/15-event-pipeline/solution/go \
	04-capstone/17-game-store-capstone/solution/go

test-all:
	@for dir in $(MODULE_DIRS); do \
		echo "==> $$dir"; \
		(cd $$dir && go test ./...) || exit 1; \
	done

test-new:
	@for dir in $(NEW_MODULE_DIRS); do \
		echo "==> $$dir"; \
		(cd $$dir && go test ./...) || exit 1; \
	done

test-migrated:
	@for dir in $(MIGRATED_MODULE_DIRS); do \
		echo "==> $$dir"; \
		(cd $$dir && go test ./...) || exit 1; \
	done

test-infra:
	@$(MAKE) -C 03-platform-engineering/16-gitops-deploy/problem docker-build
	@$(MAKE) -C 03-platform-engineering/16-gitops-deploy/problem helm-lint
	@$(MAKE) -C 03-platform-engineering/16-gitops-deploy/problem helm-template

test-runtime:
	@$(MAKE) -C 03-platform-engineering/14-cockroach-tx/solution/go repro
	@$(MAKE) -C 03-platform-engineering/15-event-pipeline/solution/go repro
	@$(MAKE) -C 04-capstone/17-game-store-capstone/solution/go repro

test-portfolio-unit:
	@(cd 05-portfolio-projects/18-workspace-saas-api/solution/go && go test ./...)

test-portfolio-repro:
	@$(MAKE) -C 05-portfolio-projects/18-workspace-saas-api/solution/go repro

check-docs:
	@find . -mindepth 2 -maxdepth 2 -type d | grep -E '/[0-9]{2}-' | while read -r dir; do \
		[ -f "$$dir/README.md" ] || { echo "missing README: $$dir"; exit 1; }; \
		[ -f "$$dir/problem/README.md" ] || { echo "missing problem README: $$dir"; exit 1; }; \
		[ -f "$$dir/solution/README.md" ] || { echo "missing solution README: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/README.md" ] || { echo "missing docs README: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/concepts/core-concepts.md" ] || { echo "missing core concepts: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/references/README.md" ] || { echo "missing references: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/verification.md" ] || { echo "missing verification: $$dir"; exit 1; }; \
		[ -f "$$dir/notion/05-development-timeline.md" ] || { echo "missing notion timeline: $$dir"; exit 1; }; \
	done
	@[ -f ../README.md ] || { echo "missing root README"; exit 1; }
	@! rg -n '확장할 자리|추가할 예정이다|미정리|placeholder|TODO' . -g '*.md' -g '!**/problem/**'
	@! rg -n 'github.com/woopinbell/go-backend/(01-foundation|02-distributed-system|03-platform-engineering|04-platform-capstone)' . -g 'go.mod' -g '*.go'

check-notion:
	@test "$$(find . -path '*/notion/*.md' -type f -size 0 | wc -l | tr -d ' ')" = "0"

release-check:
	@$(MAKE) test-all
	@$(MAKE) test-infra
	@$(MAKE) check-docs
	@$(MAKE) check-notion
