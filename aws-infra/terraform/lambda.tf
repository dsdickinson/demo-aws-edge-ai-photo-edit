resource "aws_lambda_function" "metadata_ingest" {
  function_name = "${var.project_name}-ingest"
  handler       = "app.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_role.arn
  filename      = "lambda.zip"

  source_code_hash = filebase64sha256("lambda.zip")
}
