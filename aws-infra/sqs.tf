resource "aws_sqs_queue" "image_jobs" {
  name                      = "${var.project_name}-queue"
  visibility_timeout_seconds = 60
}
