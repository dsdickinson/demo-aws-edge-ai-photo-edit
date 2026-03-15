resource "aws_lambda_function" "metadata_ingest" {
  function_name = "${var.project_name}-ingest"
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_role.arn
  filename      = "../../jetson-ai-worker/app/lambda/lambda.zip"
  source_code_hash = filebase64sha256("../../jetson-ai-worker/app/lambda/lambda.zip")
}
