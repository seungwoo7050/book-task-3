# API

## Auth

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/session`

## Admin

- `GET /api/users`
- `POST /api/users`
- `PUT /api/users/:id`
- `GET /api/settings`
- `PUT /api/settings`
- `GET /api/audit-logs`

## Catalog And Recommendation

- `GET /api/catalog`
- `GET /api/catalog/:id`
- `POST /api/catalog`
- `PUT /api/catalog/:id`
- `DELETE /api/catalog/:id`
- `POST /api/catalog/import`
- `GET /api/catalog/export`
- `POST /api/manifests/validate`
- `POST /api/recommendations`
- `POST /api/recommendations/candidate`

## Signals And Experiments

- `GET /api/usage-events`
- `POST /api/usage-events`
- `GET /api/feedback`
- `POST /api/feedback`
- `GET /api/experiments`
- `POST /api/experiments`
- `PUT /api/experiments/:id`
- `DELETE /api/experiments/:id`
- `GET /api/compare/latest`

## Release

- `GET /api/release-candidates`
- `POST /api/release-candidates`
- `PUT /api/release-candidates/:id`
- `DELETE /api/release-candidates/:id`
- `GET /api/compatibility/latest`
- `GET /api/release-gate/latest`
- `GET /api/submission/latest`

## Jobs

- `GET /api/jobs`
- `GET /api/jobs/:id`
- `POST /api/jobs/eval`
- `POST /api/jobs/compare`
- `POST /api/jobs/compatibility`
- `POST /api/jobs/release-gate`
- `POST /api/jobs/artifact-export`
