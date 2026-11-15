# backend.tf
# Configures Terraform to store state remotely in an encrypted S3 bucket with DynamoDB state locking.
#
# Pre-requisite:
# 1. Provision the S3 bucket and DynamoDB locking table (see aws-infra/terraform/bootstrap).
# 2. Run:
#      terraform init -migrate-state
#    to copy existing local state (terraform.tfstate) to the remote S3 bucket.

terraform {
  backend "s3" {
    bucket         = "demo-aws-edge-ai-photo-edit-tfstate-015283627155"
    key            = "demo-aws-edge-ai-photo-edit/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "demo-aws-edge-ai-photo-edit-tfstate-locks"
    encrypt        = true
  }
}
