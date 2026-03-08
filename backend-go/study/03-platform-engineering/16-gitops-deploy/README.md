# 16 GitOps Deploy

## Status

`verified`

## Legacy source

- legacy/03-platform-engineering/08-gitops-deploy (`legacy/03-platform-engineering/08-gitops-deploy/README.md`, not included in this public repo)

## Problem scope

- Docker multi-stage build
- Helm chart
- ArgoCD application manifest

## Build

```bash
make -C problem docker-build
```

## Test

```bash
make -C problem helm-lint
make -C problem helm-template
```

## Verification

- `make -C problem docker-build`
- `make -C problem helm-lint`
- `make -C problem helm-template`

## Known gaps

- cluster apply와 ArgoCD sync smoke test는 선택 검증으로 남긴다.
