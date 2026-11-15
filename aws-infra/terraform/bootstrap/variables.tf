variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for Terraform backend infrastructure"
}

variable "state_bucket_name" {
  type        = string
  default     = "demo-aws-edge-ai-photo-edit-tfstate-015283627155"
  description = "Globally unique S3 bucket name for storing Terraform remote state"
}

variable "lock_table_name" {
  type        = string
  default     = "demo-aws-edge-ai-photo-edit-tfstate-locks"
  description = "DynamoDB table name for Terraform state locking"
}
