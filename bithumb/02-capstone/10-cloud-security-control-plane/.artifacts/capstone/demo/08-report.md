# Cloud Security Control Plane Report

## Findings
- `CSPM-001` `HIGH` `suppressed` `study2-public-logs`: S3 bucket does not fully block public access
- `CSPM-002` `HIGH` `open` `ssh_open`: Security group exposes SSH or RDP to the internet
- `CSPM-003` `MEDIUM` `open` `study2-analytics`: Resource encryption is disabled
- `IAM-001` `HIGH` `open` `BroadAdmin`: Policy allows every action
- `IAM-002` `HIGH` `open` `BroadAdmin`: Policy applies to every resource
- `LAKE-001` `MEDIUM` `open` `CreateAccessKey`: Detected CreateAccessKey event
- `LAKE-004` `MEDIUM` `open` `DeleteTrail`: Detected DeleteTrail event
- `K8S-001` `HIGH` `open` `insecure-api`: Manifest uses hostPath volume
- `K8S-002` `MEDIUM` `open` `insecure-api`: Container uses latest tag
- `K8S-003` `HIGH` `open` `insecure-api`: Container security context is too broad

## Exceptions
- `f96987c43e4a82dc` `approved` expires `2026-03-21T05:43:30.214206+00:00` reason: Temporary business exception for demo

## Remediation Plans
- `cd605b1287dbef62` `manual_approval_required` `generated`: Dry-run remediation for CSPM-002
