# Deployment Note For ECS, RDS, And ElastiCache

## Target shape

- app: ECS Fargate service running the Spring Boot container
- database: Amazon RDS for PostgreSQL
- cache: Amazon ElastiCache for Redis
- messaging: managed Kafka alternative or self-managed Kafka-compatible broker, depending on team constraints
- secrets: AWS Secrets Manager or SSM Parameter Store
- logs and metrics: CloudWatch plus Micrometer Prometheus export when needed

## Minimal deployment flow

1. Build the image in CI.
2. Push to ECR.
3. Run Flyway migrations before or during deployment.
4. Deploy the new task definition to ECS.
5. Point the service at RDS, Redis, and the Kafka endpoint.
6. Verify `/api/v1/health/live` and `/api/v1/health/ready`.

## Environment variables to separate

- DB host, port, name, user, password
- Redis host and port
- Kafka bootstrap servers
- JWT secret
- Google OAuth client values when real OAuth is used

## What is intentionally not claimed here

- full blue/green deployment automation
- zero-downtime migration guarantees
- production traffic tuning
- live AWS validation from this repository

