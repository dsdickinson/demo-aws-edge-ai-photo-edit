variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "edge-ai-phedit-demo"
}

variable "lambda_function_name" {
  default = "image-metadata-handler"
}

variable "dynamodb_table_name" {
  default = "image-metadata"
}
