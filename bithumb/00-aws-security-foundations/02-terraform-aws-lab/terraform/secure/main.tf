terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "ap-northeast-2"
  access_key                  = "study2"
  secret_key                  = "study2"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
}

resource "aws_s3_bucket" "private_logs" {
  bucket = "study2-private-logs-example"
}

resource "aws_s3_bucket_public_access_block" "private_logs" {
  bucket                  = aws_s3_bucket.private_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_vpc" "main" {
  cidr_block = "10.10.0.0/16"
}

resource "aws_security_group" "ssh_private" {
  name        = "study2-ssh-private"
  description = "Limited ingress"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.10.10.0/24"]
  }
}

resource "aws_iam_policy" "scoped_read" {
  name = "study2-scoped-read"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::study2-private-logs-example",
          "arn:aws:s3:::study2-private-logs-example/*"
        ]
      }
    ]
  })
}

