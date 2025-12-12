variable "bucket_name" {
  type        = string
  default     = "semantiq-reports"
}

resource "aws_s3_bucket" "reports" {
  bucket = var.bucket_name
}

locals {
  bucket = aws_s3_bucket.reports.id
}

output "s3_bucket_name" {
  value = local.bucket
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.reports.arn
}
