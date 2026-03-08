.PHONY: test-all test-new test-migrated test-infra test-runtime test-portfolio-unit test-portfolio-repro check-docs check-notion release-check

MODULE_DIRS := \
	00-go-fundamentals/01-go-syntax-and-tooling/go \
	00-go-fundamentals/02-types-errors-interfaces/go \
	00-go-fundamentals/03-testing-and-debugging/go \
	01-backend-core/04-sql-and-data-modeling/go \
	01-backend-core/05-http-rest-basics/go \
	01-backend-core/06-go-api-standard/go \
	01-backend-core/07-auth-session-jwt/go \
	01-backend-core/08-sql-store-api/go \
	01-backend-core/09-cache-migrations-observability/go \
	01-backend-core/10-concurrency-patterns/go \
	01-backend-core/11-rate-limiter/go \
	02-distributed-systems/12-grpc-microservices/go \
	02-distributed-systems/13-distributed-log-core/go \
	03-platform-engineering/14-cockroach-tx/go \
	03-platform-engineering/15-event-pipeline/go \
	04-capstone/17-game-store-capstone/go \
	05-portfolio-projects/18-workspace-saas-api/go

NEW_MODULE_DIRS := \
	00-go-fundamentals/01-go-syntax-and-tooling/go \
	00-go-fundamentals/02-types-errors-interfaces/go \
	00-go-fundamentals/03-testing-and-debugging/go \
	01-backend-core/04-sql-and-data-modeling/go \
	01-backend-core/05-http-rest-basics/go \
	01-backend-core/07-auth-session-jwt/go \
	01-backend-core/08-sql-store-api/go \
	01-backend-core/09-cache-migrations-observability/go \
	05-portfolio-projects/18-workspace-saas-api/go

MIGRATED_MODULE_DIRS := \
	01-backend-core/06-go-api-standard/go \
	01-backend-core/10-concurrency-patterns/go \
	01-backend-core/11-rate-limiter/go \
	02-distributed-systems/12-grpc-microservices/go \
	02-distributed-systems/13-distributed-log-core/go \
	03-platform-engineering/14-cockroach-tx/go \
	03-platform-engineering/15-event-pipeline/go \
	04-capstone/17-game-store-capstone/go

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
	@$(MAKE) -C 03-platform-engineering/14-cockroach-tx/go repro
	@$(MAKE) -C 03-platform-engineering/15-event-pipeline/go repro
	@$(MAKE) -C 04-capstone/17-game-store-capstone/go repro

test-portfolio-unit:
	@(cd 05-portfolio-projects/18-workspace-saas-api/go && go test ./...)

test-portfolio-repro:
	@$(MAKE) -C 05-portfolio-projects/18-workspace-saas-api/go repro

check-docs:
	@find . -mindepth 2 -maxdepth 2 -type d | grep -E '/[0-9]{2}-' | while read -r dir; do \
		[ -f "$$dir/README.md" ] || { echo "missing README: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/README.md" ] || { echo "missing docs README: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/concepts/core-concepts.md" ] || { echo "missing core concepts: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/references/README.md" ] || { echo "missing references: $$dir"; exit 1; }; \
		[ -f "$$dir/docs/verification.md" ] || { echo "missing verification: $$dir"; exit 1; }; \
	done
	@! rg -n '확장할 자리|추가할 예정이다|미정리|placeholder|TODO' . -g '*.md' -g '!**/problem/**'
	@! rg -n 'github.com/woopinbell/go-backend/(01-foundation|02-distributed-system|03-platform-engineering|04-platform-capstone)' . -g 'go.mod' -g '*.go'

check-notion:
	@test "$$(find . -path '*/notion/*.md' -type f -size 0 | wc -l | tr -d ' ')" = "0"

release-check:
	@$(MAKE) test-all
	@$(MAKE) test-infra
	@$(MAKE) check-docs
	@$(MAKE) check-notion
