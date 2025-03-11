# Configure AWS Provider
provider "aws" {
  region = "us-west-2"
}

# S3 bucket with various configuration options
resource "aws_s3_bucket" "example" {
  bucket = "my-test-bucket-2025"

  tags = {
    Environment = "Test"
    Project     = "CloudBuilder"
    ManagedBy   = "Terraform"
  }
}

# Enable versioning
resource "aws_s3_bucket_versioning" "example" {
  bucket = aws_s3_bucket.example.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Bucket lifecycle rule
resource "aws_s3_bucket_lifecycle_rule" "example" {
  bucket = aws_s3_bucket.example.id
  id     = "transition-to-glacier"

  transition {
    days          = 90
    storage_class = "GLACIER"
  }

  expiration {
    days = 365
  }

  status = "Enabled"
}

# Bucket policy to enforce SSL
resource "aws_s3_bucket_policy" "example" {
  bucket = aws_s3_bucket.example.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceSSLOnly"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.example.arn,
          "${aws_s3_bucket.example.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

# Output the bucket name and ARN
output "bucket_name" {
  value = aws_s3_bucket.example.id
}

output "bucket_arn" {
  value = aws_s3_bucket.example.arn
}
