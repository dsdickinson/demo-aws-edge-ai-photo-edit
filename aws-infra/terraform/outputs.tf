output "api_endpoint" {
  value = aws_apigatewayv2_api.http_api.api_endpoint
}

output "s3_bucket" {
  value = aws_s3_bucket.raw_images.bucket
}

output "sqs_queue_url" {
  value = aws_sqs_queue.image_jobs.url
}

