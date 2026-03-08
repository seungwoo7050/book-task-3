.PHONY: help docker-build docker-push helm-lint helm-template helm-install argocd-apply

IMAGE_NAME ?= go-backend-api
IMAGE_TAG ?= latest
REGISTRY ?= ghcr.io/woopinbell
DOCKER_CONTEXT ?= ../../..

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

docker-build: ## Build Docker image
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG) -f ../infra/Dockerfile $(DOCKER_CONTEXT)

docker-push: ## Push Docker image to registry
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

helm-lint: ## Lint the Helm chart
	helm lint ../infra/charts/go-backend

helm-template: ## Render Helm templates locally
	helm template go-backend ../infra/charts/go-backend

helm-install: ## Install/upgrade the Helm chart
	helm upgrade --install go-backend ../infra/charts/go-backend \
		--namespace default \
		--wait

argocd-apply: ## Apply ArgoCD Application manifest
	kubectl apply -f ../infra/k8s/argocd-app.yaml
