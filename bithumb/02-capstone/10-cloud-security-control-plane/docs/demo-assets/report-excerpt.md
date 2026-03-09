# Report Excerpt

## Findings

- `CSPM-001` `HIGH` `suppressed` `study2-public-logs`: S3 bucket does not fully block public access
- `CSPM-002` `HIGH` `open` `ssh_open`: Security group exposes SSH or RDP to the internet
- `IAM-001` `HIGH` `open` `BroadAdmin`: Policy allows every action
- `LAKE-004` `MEDIUM` `open` `DeleteTrail`: Detected DeleteTrail event
- `K8S-003` `HIGH` `open` `insecure-api`: Container security context is too broad

## Exceptions

- `CSPM-001` finding is temporarily suppressed by an approved exception.

## Remediation Plans

- `CSPM-002` has a dry-run remediation plan that narrows public ingress before any destructive apply.
